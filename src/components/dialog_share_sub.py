import streamlit as st
import segno #for qr
import io #to handle binary data


@st.dialog("Share Class")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "attendify.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"
    
    # st.header("Scan to Join") 
    
    qr = segno.make(join_url) 
    
    out = io.BytesIO() #place to save qr
    qr.save(out, kind="png" , scale=10, border=1)
    
    c1, c2 = st.columns([3, 2]) 
    
    with c1:
        st.caption("Class link")
        st.code(join_url, language=None)
        st.caption("Class code")
        st.code(subject_code, language=None)
        st.caption("Send the link on WhatsApp or email.")
        
    with c2:
        st.image(out.getvalue(), caption="Scan to join", width="stretch" )
    
    
  
            




