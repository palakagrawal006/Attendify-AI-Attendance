import streamlit as st
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.screens.home_screen import home_screen
from src.components.dialog_autoenroll import auto_enroll_dialog


def main():
    
    st.set_page_config(
    page_title="Attendify | AI Attendance",
    page_icon="assets/attendify_icon.png",
    layout="centered",
    )
    
    
    # initialise 
    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None #initially no one logged in - home pg
        
    match st.session_state["login_type"]:    #switch case
        case "teacher":
            teacher_screen() 
        case "student":
            student_screen() 
        
        case None :
            home_screen() 
        
    
    join_code = st.query_params.get('join-code') 
    
    if join_code :
        # login type student nhi h , to banao , or rerun hokr login pg open hojayega , from above code
        if st.session_state.get("login_type") != "student":
            st.session_state["login_type"] = "student"
            st.rerun() 
           
        #    already logged in as student
        if st.session_state.get("is_logged_in")  and st.session_state.get("user_role") == 'student' :
            auto_enroll_dialog(join_code)
            

main()