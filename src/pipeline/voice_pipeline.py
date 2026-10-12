from resemblyzer import VoiceEncoder, preprocess_wav  #to again preprocess- normalize audio 
import numpy as np
import io #same as pillow(PIL) in img - help audio to load in librosa 
import librosa #to edit audio 
import streamlit as st 



@st.cache_resource 
def load_voice_encoder(): #model 
    return VoiceEncoder()



def get_voice_embedding(audio_byte):
    try:
        encoder = load_voice_encoder() 
        
        audio , sr = librosa.load(io.BytesIO(audio_byte) , sr=16000) #sr - sample rate -high - utna accha audio 
        wav = preprocess_wav(audio)  #normalized and trim silence
        embedding = encoder.embed_utterance(wav) #give embeddings
        return embedding.tolist()  #256D
        
    except Exception as e:
        st.error(f"Voice processing error: {e}")
        return None
    

# identify speaker 
def identify_speaker (new_embedding , candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict :
        return None, 0.0 # student_id, score
    
    new_embedding = np.asarray(new_embedding)
    best_sid  = None # stu_id
    best_score = -1.0
    
    for sid , stored_embedding in  candidates_dict.items():
        if stored_embedding:
            similarity  = np.dot(new_embedding, np.asarray(stored_embedding))
            
            if similarity > best_score:
                best_score = similarity
                best_sid = sid
    
    if best_score >= threshold:
        return  best_sid , best_score
    
    return None , best_score #-1 


# bulk - teacher ek mike se multiple audios
def process_bulk_audio (audio_bytes , candidates_dict, threshold=0.65):
    
    try:
        encoder = load_voice_encoder() 
        
        audio , sr = librosa.load(io.BytesIO(audio_bytes) , sr=16000)
        segments = librosa.effects.split(audio , top_db=30) # top_db - sensitivity(vol) of voice
        
        identified_results = {} #s_id
        
        for start, end in segments :
            if (end-start) < sr * 0.5 : #too low sound/noise/garbage
                continue 
            
            segment_audio  = audio[start:end] #preprocess- trim 
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav) 
                            
            sid, score = identify_speaker(embedding, candidates_dict, threshold )
                      
            if sid is not None and (sid not in identified_results or score > identified_results[sid]):
                identified_results[sid] = score 
                    
        return identified_results

    except Exception as e:
         st.error(f"Bulk process error: {e}")
         return {}
        
                    