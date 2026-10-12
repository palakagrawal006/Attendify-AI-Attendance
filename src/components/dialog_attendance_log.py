
import streamlit as st
from src.database.db import create_attendance


def show_attendance_result (df, logs,  clear_keys=()):
    st.write("Please review attendance before confirming.")
    st.dataframe(df, hide_index=True , width="stretch") 
    
    def _reset():
        for k in clear_keys:
            st.session_state.pop(k, None)
    
    c1 , c2 = st.columns(2)
    
    with c1 :
        if st.button("Discard", width="stretch") :
            _reset()
            st.rerun()
        
    with c2:
        if st.button("Confirm & Save", width="stretch", type='primary') :
            try:
                with st.spinner("Finalising attendance... "):
                    create_attendance(logs)       
            except Exception as e :
                st.error(f'Sync failed : {e}')
            else :
                st.toast("Attendance taken") 

                #emptying after creating atten and showing
                _reset()      
                st.rerun()

@st.dialog("Attendance Reports")
def attendance_result_dialog(df , logs):
    show_attendance_result(df , logs, clear_keys=["attendance_images"]) 
