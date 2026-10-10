import streamlit as st
from pathlib import Path
from src.database.db import get_teacher_subjects
from src.components.dialog_create_sub import create_sub_dialog
from src.components.dialog_share_sub import share_subject_dialog
from src.components.subject_card import subject_card 



# def attendance_tab(teacher):
#     st.subheader("Take AI attendance")
#     subjects = get_subjects(teacher["teacher_id"])

#     if not subjects:
#         st.info("You haven't created any subjects yet. Create a subject first.")
#         st.button("Create a subject", icon=":material/add:", on_click=set_tab, args=("subjects",))
#         return

#     subject = st.selectbox("Subject", subjects, format_func=lambda s: s["name"])
#     photo = st.camera_input("Take a photo of the class")
#     if photo:
#         st.write("Next step: run predict_attendance on this photo and save the result.")

# ------------------------------------------------

def manage_subject(teacher):
    teacher_id = st.session_state.teacher_data['teacher_id'] 
    c1, c2 = st.columns([4, 2]) 
    
    with c1:
        st.subheader("Manage subjects", width="stretch") 
    
    with c2 :
        if st.button("+ Create New Subject" , width='stretch'  ,type="primary"):
            create_sub_dialog(teacher_id) 
            
    st.space()
    # list all subjects
    
    subjects = get_teacher_subjects(teacher_id) 
    
    if subjects:
        for sub in subjects :
            stats = [
                ("Students" , sub["total_students"] ),
                ("Classes" , sub["total_classes"] ),
            ]
        
            def share_button():
                if st.button(f"Share Code" , key = f"share_{sub['subject_code']}", icon=":material/share:" , width="stretch"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
            
            subject_card (
                name = sub['name'],
                code  = sub['subject_code'],
                section = sub['section'],
                stats = stats , #extra info 
                footer_callback = share_button
            )
    
    else :
        st.info("No Subjects found. Create One above")
            
    
# -------------------------------------------------------------------

# def records_tab(teacher):
#     st.subheader("Attendance records")
#     st.info("No records yet. They appear here once you take attendance.")

# -------------------------------------------------------------------

def teacher_dashboard():
    teacher = st.session_state["teacher_data"]
    st.markdown(f"### Welcome, :primary[{teacher['name']}]")
    

    # if "current_teacher_tab" not in st.session_state :
    #     st.session_state["current_teacher_tab"] = "take_attendance"
    current = st.session_state.setdefault("current_teacher_tab", "take_attendance")
             
    TABS = [ #key , label , icon 
    ("take_attendance",   "Take Attendance",   ":material/ar_on_you:"),
    ("manage_subjects",   "Manage Subjects",   ":material/book_ribbon:"),
    ("attendance_report", "Attendance Report", ":material/cards_stack:"),
    ]

    for col, (key, label, icon) in zip(st.columns(3), TABS):
        with col:
            if st.button(label, key=f"tab_{key}", icon=icon, width="stretch",
                         type="primary" if current == key else "tertiary"):
                st.session_state["current_teacher_tab"] = key
                st.rerun()

    st.divider()
    
    if current == "take_attendance":
        st.write("Hello")
        # attendance_tab(teacher)       # the three tab functions from my last message
    elif current == "manage_subjects":
        manage_subject(teacher)
    else:
        # records_tab(teacher)
        st.write("Hello")
        