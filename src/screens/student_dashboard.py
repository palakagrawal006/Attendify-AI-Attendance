
import streamlit as st
from pathlib import Path
from src.database.db import get_student_subjects, get_student_attendance
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card 
from src.database.db import unenroll_student_to_subject



def student_dashboard():
    student = st.session_state["student_data"]
    student_id = student['student_id']
    
    st.markdown(f"### Welcome, :primary[{student['name']}]")

    c1, c2 = st.columns([4, 2], vertical_alignment="center")
    with c1:
        st.subheader("Your enrolled subjects")
    with c2:
        if st.button("+ Enroll in subject", type="primary", width="stretch"):
            enroll_dialog()

    st.divider()
    
    with st.spinner("Loading your subjects..."):
        subjects = get_student_subjects(student_id) 
        logs =  get_student_attendance(student_id)    #attendance - log of all subject jisme wo enroll h 
        
    stats_map ={}
    
    for log in logs : #jb jb jis sub ki class hui h 
        sid = log['subject_id']
        
        s =stats_map.setdefault(sid, {"total": 0, "attended": 0})
        s["total"] += 1
        if log.get("is_present"):
            s["attended"] += 1
            
    if not subjects:
        st.info("You haven't enrolled in any subject yet. Use the button above "
                "with the code from your teacher.")
        return
    
    cols = st.columns(2) 
    
    for  sub_node in subjects:
        sub = sub_node["subjects"] 
        sid = sub["subject_id"] 
        
        stats = stats_map.get(sid , {"total":0, "attended":0} ) # if else  
        
        def unenroll_btn():
            if st.button("Unenroll" , key=f"unenroll_{sid}", icon=":material/delete_forever:",  width='stretch'):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenrolled from {sub['name']} succesfully!")
                st.rerun()
        
      
        subject_card(
            name = sub['name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats = [
                ('Classes', stats['total']),
                ('Attended', stats['attended']),
                ] ,
            footer_callback = unenroll_btn ,
        )