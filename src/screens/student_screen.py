import streamlit as st
from pathlib import Path
from src.components.header import header   # make sure this name matches header.py
from src.components.footer import footer
from src.ui.style_base_layout import style_base_layout
from src.database.db import create_teacher, check_teacher_exists, teacher_login

def auth_style():
    css = (Path(__file__).parent.parent / "ui" / "auth.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)



def student_screen():
    header()
    style_base_layout()
    auth_style()

    # back link: top-left, under the header, in its own narrow row
    back_col, _ = st.columns([1, 5])
    with back_col:
        if st.button("Back to home", key="back_home", type="tertiary",
                  icon=":material/arrow_back:") :
            st.session_state["login_type"] = None
        
    
    st.header("Login using FaceId", text_alignment="center") 
    st.camera_input("Position your face in the center")
   

    footer()
   
        
