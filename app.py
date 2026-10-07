import streamlit as st
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.screens.home_screen import home_screen


def main():
    
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
        
main()