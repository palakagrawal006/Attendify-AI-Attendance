import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase 


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(join_code):
    student_id = st.session_state["student_data"]["student_id"]


    res = (supabase.table("subjects").select("subject_id, name")
        .eq("subject_code", join_code).execute())
    if not res.data:
        st.error("No subject found with that code.")
        if st.button("Close") :
            st.query_params.clear()
            st.rerun()
        return 
    
    subject = res.data[0] 
                
    already = (supabase.table("subject_student").select("student_id")
                .eq("subject_id", subject["subject_id"])
                .eq("student_id", student_id).execute())
    if already.data:
        st.info("You are already enrolled in this subject.")
        if st.button("Got it!") :
            st.query_params.clear()
            st.rerun()
        return 

    st.markdown(f"Would you like to enroll in  **{subject['name']}**?")
    
    c1, c2  = st.columns(2) 
    with c1 : 
        if st.button("No Thanks!", width='stretch') :
            st.query_params.clear()
            st.rerun() 
    with c2: 
        if st.button("Yes enroll now!", type="primary" , width='stretch') :
            try:
                enroll_student_to_subject(student_id, subject["subject_id"])
            except Exception as e:
                st.error(f"Could not enroll: {e}")
            else:
                st.toast(f"Enrolled in {subject['name']}")
                st.query_params.clear()
                st.rerun()
                
            