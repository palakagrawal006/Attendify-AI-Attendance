
import streamlit as st
import dlib 
import numpy as np 
import face_recognition_models
from sklearn.svm  import SVC

from src.database.db import get_all_students


@st.cache_resource  #load only once- very heavy 
def load_dlib_models():
    detector =  dlib.get_frontal_face_detector() 
    
    # shape predictor
    sp =  dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location() #face points
    )
    
    # face recognitiion
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    
    return detector, sp , facerec 



def get_face_embeddings (image_np):
    detector, sp , facerec = load_dlib_models()
    
    faces = detector(image_np, 1) #1 image only 1 time
    
    encodings = []
    
    for face in faces :
        shape = sp(image_np, face) #landmarks- 68
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #embeddings - 128
        
        encodings.append(np.array(face_descriptor)) 
        
    return encodings 
# image in number format 



# take all photos of student from database and train model (svc)
@st.cache_resource  #load only once- very heavy 
def get_trained_model():
    X =[] #embeddings of all students in database
    y = []  #id of all stu 
    
    student_db = get_all_students()
    
    if not student_db :
        return None 
    
    for student in student_db :
        embedding = student.get('face_embedding') 
        if embedding:
            X.append(np.array(embedding)) 
            y.append(student.get('student_id')) 
            
    if len(X)== 0 :
        return None
    
    # CLASSIFICATION - with straight line
    # kernel = function to classify , prob of this person , class wt = scale all photos - if 1 person have multiple photos 
    clf = None
    if len(set(y)) >= 2:          # SVC needs at least 2 students
        clf = SVC(kernel="linear", class_weight="balanced")
        clf.fit(X, y)

    return {"clf": clf, "X": np.array(X), "y": y}    # X as an array
    


"""Call after a new student is added."""
def train_classifier():
        get_trained_model.clear() 
        model_data = get_trained_model()
        return bool(model_data)
    
# group photo
def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected = {}

    model = get_trained_model()
    if not model:
        return detected, [], len(encodings) #embeddings, students, no of stu 
    
    clf, X, y = model["clf"], model["X"], model["y"]
    all_students = sorted(set(y))

    for encoding in encodings:
        if clf:
            pred_id = int(clf.predict([encoding])[0])#sbse zyda score wala
        else:
            pred_id = int(all_students[0])  # only one student enrolled

        # id mil gyi - ab encoding - x train and y train have val in same idx 
        # compare with ALL photos of that student, keep the closest
        idx = [i for i, sid in enumerate(y) if sid == pred_id]
        distance = np.linalg.norm(X[idx] - encoding, axis=1).min()

        resemblance_score = 0.6 #max diff 
        if distance <= resemblance_score:
            detected[pred_id] = True

    return detected, all_students, len(encodings)