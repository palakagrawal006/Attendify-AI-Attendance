from src.database.config import supabase 
import bcrypt

# teacher registration 
def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode() , hashed.encode())

def check_teacher_exists(username):
    # check for unique username, return true when username is already taken 
    response = supabase.table("teachers").select("username").eq("username", username).execute() 
    return len(response.data) > 0


def create_teacher(username, password, name ):
    # hash password 
    data = {
        "username" : username , 
        "password" : hash_pass(password) ,
        "name" :name , 
    }
    response = supabase.table("teachers").insert(data).execute()
    return response 


# teacher login 
def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute() #CHECK if username exists
     
    if not response.data:
        return None

    teacher = response.data[0] 
    
    if check_pass(password, teacher["password"]) :
        return teacher
    return None 


def create_subject(sub_id, sub_name, sub_section, teacher_id):
    data ={
        "subject_code":sub_id, 
        "name":sub_name, 
        "section":sub_section, 
        "teacher_id":teacher_id
        }
    
    response = supabase.table("subjects").insert(data).execute()
    return response.data 


def get_teacher_subjects(teacher_id):
    response = (
        supabase.table("subjects")
        .select("*, subject_student(count), attandance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    subjects = response.data

    for sub in subjects:
        counts = sub.pop("subject_student", [])
        sub["total_students"] = counts[0]["count"] if counts else 0

        logs = sub.pop("attandance_logs", [])
        sub["total_classes"] = len({log["timestamp"] for log in logs})

    return subjects


# student screen 
def  get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data


def create_student(name, face_embedding=None , voice_embedding=None):
    data = {
        'name' : name ,
        'face_embedding' : face_embedding,
        'voice_embedding' : voice_embedding 
    }
    
    response = supabase.table("students").insert(data).execute()
    return response.data


# enroll in subj
def enroll_student_to_subject(student_id, subject_id):
    data = {
        'student_id' : student_id,
        'subject_id' : subject_id 
    }
    response = supabase.table("subject_student").insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table("subject_student").delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data

    
def get_student_subjects(student_id):
    response = supabase.table("subject_student").select("*, subjects(*)").eq('student_id' , student_id).execute()
    return response.data
    
    
def get_student_attendance(student_id):
    response = supabase.table("attandance_logs").select("*, subjects(*)").eq('student_id' , student_id).execute()
    return response.data


# attendance
def create_attendance(logs) :
    res = supabase.table("attandance_logs").insert(logs).execute()
    return res.data

# to show record
def get_attendance_for_teacher(teacher_id):
    res = supabase.table("attandance_logs").select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute() 
    # attandance_logs - no teacher id - inner join by - subjects id 
    return res.data