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
    