import streamlit as st
from pathlib import Path
from src.components.header import header   # make sure this name matches header.py
from src.components.footer import footer
from src.ui.style_base_layout import style_base_layout
from PIL import Image
import numpy as np 

from src.pipleline.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipleline.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student
from src.screens.student_dashboard import student_dashboard



def auth_style():
    css = (Path(__file__).parent.parent / "ui" / "auth.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# back button
def go_home():
    st.session_state["login_type"] = None

# -------------------------------------------------------------------
def login_student(student: dict):
    # never keep embeddings in session state
    student = {k: v for k, v in student.items()
               if k not in ("face_embedding", "voice_embedding")}
    st.session_state["user_role"] = "student"
    st.session_state["student_data"] = student
    st.session_state["is_logged_in"] = True
    st.toast(f"Welcome, {student['name']}")
    st.rerun()

# -------------------------------------------------------------------
def register_new_student(img):
    st.info("We couldn't match your face. New here? Register with this photo, "
            "or retake it if the lighting was bad.")

    with st.container(border=True, key="card_auth"):
        
        st.subheader("Register new Profile")
        name = st.text_input("Full name", placeholder="Amisha", key="stu_reg_name")
        
        st.caption("Optional: voice enrollment, for voice-only attendance")
        
        audio_data = None
        try:
            audio_data = st.audio_input("Record a short phrase, like: My name is Amisha, I am present.",
            key="stu_reg_audio",)
        except Exception:
            st.error("Audio Data Failed") 
            
        if st.button("Create Account" , type="primary", width="stretch",
                     icon=":material/person_add:", key="stu_reg_submit"):
            if not name.strip() :
                st.error("Enter your name.")
                return
            
            with st.spinner("Creating profile..."):
                encodings = get_face_embeddings(img) 
                
                if len(encodings) != 1: #no. of faces
                    st.error("Exactly one face must be visible. Retake the photo.")
                    return
                
                face_emb = encodings[0].tolist() 
                
                voice_emb = None 
                if audio_data :
                    voice_emb = get_voice_embedding(audio_data.getvalue())
                
                try:
                     response_data = create_student(name.strip(), face_embedding = face_emb , voice_embedding=voice_emb)
                except Exception as e:
                    st.error(str(e))
                    return

                    
                if response_data:
                    train_classifier()          # retrain so the new face is recognized next time
                    login_student(response_data[0])
                
                else :
                    st.error("Couldn't create your profile. Try again.")


# -------------------------------------------------------------------

def face_login():
    st.markdown(
        """
    <div class="auth-head">
    <div class="auth-badge">STUDENT PORTAL</div>
    <div class="auth-title">Welcome <span>back</span></div>
    <div class="auth-sub">Login using Face ID.</div>
    </div>
    """,
            unsafe_allow_html=True,
        )
    photo = st.camera_input("Position your face in the center")
    if not photo:
        return

    img = np.array(Image.open(photo).convert("RGB"))

    with st.spinner("AI is scanning..."):
        detected, all_ids, num_faces = predict_attendance(img)

    if num_faces == 0:
        st.warning("No face found. Move closer and face the camera.")
    elif num_faces > 1:
        st.warning("Multiple faces found. Only one person can log in at a time.")
    elif not detected:
        # st.error("Face not recognized.You might be a new student!")
        register_new_student(img)
        
    else:
        student_id = list(detected.keys())[0]  
        all_student = get_all_students() 
                    
        student =  next((s for s in all_student if s['student_id']== student_id), None)
        
        if student:
            login_student(student)

# -------------------------------------------------------------------
def student_logout():
    for key in ("student_data", "user_role", "is_logged_in"):
        st.session_state.pop(key, None)
    st.session_state["login_type"] = None
    st.rerun()

# -------------------------------------------------------------------
def student_screen():
    if "student_data" in st.session_state: 
        header(on_logout=student_logout)   
    else :
        header()  
        
    style_base_layout()
    auth_style()
    
    if st.session_state.get("user_role") == "student" and "student_data" in st.session_state:
        student_dashboard()

    else:
        back_col, _ = st.columns([2, 8])
        with back_col:
            st.button("Back to home", key="back_home", type="tertiary",
                      icon=":material/arrow_back:", on_click=go_home)
        face_login()
        
        
    footer()
   