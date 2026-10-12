import streamlit as st
from pathlib import Path
from src.database.db import get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_sub import create_sub_dialog
from src.components.dialog_share_sub import share_subject_dialog
from src.components.subject_card import subject_card 
from src.components.dialog_add_photos import add_photos_dialog 
from src.components.dialog_attendance_log import attendance_result_dialog 
from src.components.dialog_voice_attendance import voice_attendance_dialog 
from src.pipeline.face_pipeline import predict_attendance 
import numpy as np
import pandas as pd
from src.database.config import supabase 
from datetime import datetime


def attendance_tab(teacher_data):
    teacher_id = st.session_state.teacher_data['teacher_id'] 
    st.subheader("Take AI attendance")
    st.space()
    # store images for attendance 
    if 'attendance_images' not in st.session_state :
        st.session_state.attendance_images = []
         
    subjects = get_teacher_subjects(teacher_id) 

    if not subjects:
        st.info("You haven't created any subjects yet. Create a subject first.")
        return
    
    #  "dva-AL603 : 5"
    subject_options = {f"{s['name']} - {s['subject_code']}" : s['subject_id'] for s in subjects} #dictionary of subjects
    
    c1, c2 = st.columns([3,1], vertical_alignment='bottom') 
    
    with c1:
        selected_subject =  st.selectbox('Select Subject', options=list(subject_options.keys()))
    
    with c2 : 
        if st.button("Add Photos", type='primary', icon=':material/photo_prints:'):
            add_photos_dialog()
            
    selected_subject_id = subject_options[selected_subject]
    
    st.divider() 
    
    # preview of added photos
    if st.session_state.attendance_images : 
        st.header('Added Photos')
        gallery_cols = st.columns(4) 
        
        for idx , img in enumerate(st.session_state.attendance_images):
            with gallery_cols [idx % 4] :
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
       

    # bottom ribbon 
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3) 
    
    with c1 :
        if st.button("Clear all photos" , width='stretch', type='tertiary', icon=":material/delete:" ,disabled=not has_photos) :
            st.session_state.attendance_images = []
            st.rerun() 
            
    with c2 :
        if st.button("Run Face Analysis" , width='stretch', type='primary', icon=":material/analytics:" ,disabled=not has_photos) :
            with st.spinner("Deep scanning classroom photos..."):
                all_detected_ids = {} 
                
                for i , img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img) 
                    detected , _, _ = predict_attendance(img_np) 
                    
                    if detected:
                        for sid  in detected.keys( ) :
                            student_id = int(sid) 
                            
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {i+1}") #to save in which photo no. that student appears
                            
                # find list of all student enrolled in that subject 
                enrolled_res = supabase.table("subject_student").select("*, students(*)").eq('subject_id' , selected_subject_id).execute()
                
                enrolled_student = enrolled_res.data
                if not enrolled_student :
                    st.warning("No students enrolled in this course")
                
                else : 
                    # results = to show in table, attendance_log = for entry in log table
                    
                    results, attendance_to_log = [], [] 
                    
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    
                    for node in enrolled_student:
                        student = node["students"] 
                        source = all_detected_ids.get(int(student['student_id']), [])  #agr present h to kis photo m present h
                        is_present = len(source)>0 
                        
                        results.append({
                            "Name": student['name'],
                            "Id" : student["student_id"] ,
                            "Source" : ", ".join(source) if is_present else "-",
                            "Status" : "✅ Present" if is_present else "❌ Absent"   
                        })
                        
                        attendance_to_log.append({
                            "student_id" : student["student_id"] ,
                            "subject_id" : selected_subject_id ,
                            "timestamp" : current_timestamp,
                            "is_present" : bool(is_present) 
                        })
                
                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
                        
    # voice attendance
    with c3:
        if st.button("Use Voice Attendance" , type="secondary", width='stretch', icon=":material/mic:") :
            voice_attendance_dialog(selected_subject_id)
        

# -----------------------------------------------------------

def manage_subject(teacher_data):
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

def attendance_record(teacher):
    st.subheader("Attendance records")
    st.space()
    
    teacher_id = teacher['teacher_id']
    
    # uss teacher k saree records atten k 
    records = get_attendance_for_teacher(teacher_id)
    
    if not records :
        st.info("No records yet. They appear here once you take attendance.")
        return 
    
    df = pd.DataFrame([
        {
            "timestamp": r.get("timestamp"),
            "Subject": r["subjects"]["name"],
            "Subject Code": r["subjects"]["subject_code"],
            "is_present": bool(r.get("is_present", False)),
        }
        for r in records
    ])

    # parse once; handles with/without milliseconds and offsets
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"])
    df["timestamp"] = df["timestamp"].dt.tz_convert("Asia/Kolkata")

    # one class = one timestamp (to the second)
    df["ts_group"] = df["timestamp"].dt.floor("s")

    summary = (
        df.groupby(["ts_group", "Subject", "Subject Code"])
        .agg(Present=("is_present", "sum"), Total=("is_present", "count"))
        .reset_index()
        .sort_values("ts_group", ascending=False)
    )

    summary["Time"] = summary["ts_group"].dt.strftime("%Y-%m-%d %I:%M %p")
    summary["Attendance Stats"] = (
        "✅ " + summary["Present"].astype(str) + " / " + summary["Total"].astype(str) + " students"
    )

    st.dataframe(
        summary[["Time", "Subject", "Subject Code", "Attendance Stats"]],
        use_container_width=True,
        hide_index=True,
    )
    
    
    # data = []
    
    # for r in records : 
    #     ts = r.get('timestamp') #ek class 1 timestamp pr hoti h 
        
    #     data.append({
    #         "ts_group": ts.split(".")[0] if ts else None, # '.' ->milisecond 
    #         "Time" : datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A" ,
    #         "Subject" : r['subjects']['name'],
    #         "Subject Code": r['subjects']['subject_code'],
    #         "is_present" : bool(r.get('is_present' , False))
    #     })
        
    # df = pd.DataFrame(data)  
    
    # summary =(
    #     df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
    #     .agg(
    #         Present_Count = ('is_present', 'sum') ,
    #         Total_Count = ('is_present', 'count') 
    #     ).reset_index()
    # )
    
    # summary['Attendance Stats'] = ( #new col 
    #     "✅" + summary['Present_Count'].astype(str) +" /" + summary['Total_Count'].astype(str) + 'Students'
    # )
    
    # display_df = (summary.sort_values(by='ts_group', ascending=False)
    #               [['Time','Subject', 'Subject Code' , 'Attendance Stats']])   #col name we want 
    
    
    # st.dataframe(display_df, width='stretch' , hide_index=True )
        
    
    

# -----------------------------------------------------------------

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
        attendance_tab(teacher)       # the three tab functions from my last message
    elif current == "manage_subjects":
        manage_subject(teacher)
    else:
        attendance_record(teacher)
        