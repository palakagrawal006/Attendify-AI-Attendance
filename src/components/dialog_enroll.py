import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase 


@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write("Enter the subject code and section your teacher gave you.")
    code = st.text_input("Subject code", placeholder="AL701")
    section = st.text_input("Section", placeholder="A")

    if st.button("Enroll now", type="primary", width="stretch"):
        code, section = code.strip().upper(), section.strip().upper()
        if not code or not section:
            st.warning("Enter both the subject code and the section.")
            return

        res = (supabase.table("subjects").select("subject_id, name")
               .eq("subject_code", code).eq("section", section).execute())
        if not res.data:
            st.error("No subject found with that code and section.")
            return

        subject = res.data[0]
        student_id = st.session_state["student_data"]["student_id"]

        already = (supabase.table("subject_student").select("student_id")
                   .eq("subject_id", subject["subject_id"])
                   .eq("student_id", student_id).execute())
        if already.data:
            st.warning("You are already enrolled in this subject.")
            return

        enroll_student_to_subject(student_id, subject["subject_id"])
        st.toast(f"Enrolled in {subject['name']}")
        st.rerun()