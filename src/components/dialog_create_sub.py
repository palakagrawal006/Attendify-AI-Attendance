import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_sub_dialog(teacher_id):
    st.write("Enter the details of new subject") 
    
    sub_id = st.text_input("Subject Code" , placeholder="AL701") 
    sub_name = st.text_input("Subject Name" , placeholder="Computer Vision") 
    sub_section = st.text_input("Section" , placeholder="A") 
    
    if st.button("Create Subject Now", type="primary", width="stretch"):
        sub_id, sub_name, sub_section = sub_id.strip().upper(), sub_name.strip(), sub_section.strip().upper()
        
        if sub_id  and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("Subject Created Succesfully")
                st.rerun()
            except Exception as e :
                st.error(f"Error : {str(e)}")
        
        else :
            st.warning("Please fill all the fields")
            
