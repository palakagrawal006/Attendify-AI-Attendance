
import streamlit as st
from src.pipeline.voice_pipeline import process_bulk_audio 
from src.database.config import supabase 
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_log   import show_attendance_result


@st.dialog("Voice Attendance")
def voice_attendance_dialog(subject_id):
    st.write("Record audio of students saying 'I am present'. The AI will recognize the students.")
    
    # audio_data = None 
    audio_data = st.audio_input("Record classroom audio")
    
    if st.button("Analyze Audio", type='primary', width='stretch',  disabled=audio_data is None) :
        with st.spinner("Processing audio data..."):
        # find list of all student enrolled in that subject 
            enrolled_res = supabase.table("subject_student").select("*, students(*)").eq('subject_id' , subject_id).execute()
            
            enrolled_student = enrolled_res.data
            if not enrolled_student :
                st.warning("No students enrolled in this course")
                return 
            
            canditates_dict = { #student_id, voice_encoding
                s["students"]["student_id"] : s["students"]["voice_embedding"] #map
                for s  in enrolled_student if s["students"].get('voice_embedding')
            }
            
            if not canditates_dict:
                st.error("No enrolled students have voice profiles registered")
                return 
            
            audio_bytes =  audio_data.read() 
            
            detected_scores = process_bulk_audio(audio_bytes,canditates_dict )
            
            results, attendance_to_log = [], [] 
                    
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            
            for node in enrolled_student:
                student = node["students"] 
                sid = student['student_id'] 
                score = detected_scores.get(sid, 0.0)
                is_present = bool(score)
                
                results.append({
                    "Name": student['name'],
                    "Id" : sid,
                    "Source" : f"{score:.2f}" if is_present else "-",
                    "Status" : "✅ Present" if is_present else "❌ Absent"   
                })
                
                attendance_to_log.append({
                    "student_id" : sid ,
                    "subject_id" : subject_id ,
                    "timestamp" : current_timestamp,
                    "is_present" : bool(is_present) 
                })
        
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)
        
        
    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs , clear_keys=["voice_attendance_results"])
              
        # clear_keys  = ist of st.session_state keys that the component should delete when the user finishes (Discard or successful Save)
    
    

