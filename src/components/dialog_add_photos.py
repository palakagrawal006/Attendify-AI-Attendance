import streamlit as st
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance")
    
    st.session_state.setdefault("photo_widget_n", 0)
    n = st.session_state["photo_widget_n"]
 
    
    t1, t2 = st.tabs(["Camera" , 'Upload Photos'])
    
    with t1: 
        # st.button("Camera" , type='' , width='stretch' ) 
        cam_photo = st.camera_input("Take Picture", key=f"dialog_cam_{n}" )
        if cam_photo:
            # with st.spinner("Adding it.. "):
                st.session_state.attendance_images.append(Image.open(cam_photo).convert("RGB"))
                st.session_state["photo_widget_n"] += 1
                st.toast('Photo Captured')
                st.rerun(scope="fragment") #to not close dialog, rerun dialog only
    
    with t2: 
        uploaded_files = st.file_uploader('Choose image files' , type=['jpg' , 'png', 'jpeg'], accept_multiple_files=True , key=f"dialog_upload_{n}") 
    
        if uploaded_files:
            # with st.spinner("Uploading it.. "):
                for f in uploaded_files :
                    st.session_state.attendance_images.append(Image.open(f).convert("RGB"))
                st.session_state["photo_widget_n"] += 1
                st.toast(f"{len(uploaded_files)} photo(s) uploaded")
                st.rerun(scope="fragment")
        
    
    st.divider() 
    st.caption(f"{len(st.session_state.attendance_images)} photo(s) added so far")
    
    if st.button("Done" , type='primary', width='stretch' ):
        st.rerun() 
    