from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import librosa
import hashlib
from tempfile import NamedTemporaryFile
from .singlestore_project1 import get_singlestore_connection
import json
import traceback
import numpy as np
from scipy.spatial.distance import cosine

router = APIRouter()

# Helper function to process the audio file and return MFCC vector
def process_voice(file_path: str) -> np.ndarray:
    y, sr = librosa.load(file_path, sr=None)  # Load with original sample rate
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    flat_mfcc = mfcc.flatten()  # Flatten the MFCC matrix into a 1D vector
    return flat_mfcc  # Return the raw MFCC vector

# Function to calculate cosine similarity between two vectors
def cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

# FastAPI route to handle voice auth signup via HTTP POST
@router.post("/api/voice-auth/signup")
async def signup(
    password: str = Form(...),
    voice_1: UploadFile = File(...),
    voice_2: UploadFile = File(...),
    voice_3: UploadFile = File(...)
):
    voice_files = [voice_1, voice_2, voice_3]
    voice_vectors = []

    try:
        for idx, voice_file in enumerate(voice_files):
            with NamedTemporaryFile(delete=True, suffix=".wav") as temp_file:
                contents = await voice_file.read()
                temp_file.write(contents)
                temp_file.flush()

                # Process the voice and generate an MFCC vector
                voice_mfcc_vector = process_voice(temp_file.name)
                voice_vectors.append(voice_mfcc_vector.tolist())
                print(f"Voice vector {len(voice_vectors)} received")

        # Store the password and MFCC vectors in SingleStore
        connection = get_singlestore_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO users (password, voice_hash_1, voice_hash_2, voice_hash_3)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (password, json.dumps(voice_vectors[0]), 
                                    json.dumps(voice_vectors[1]), json.dumps(voice_vectors[2])))
                connection.commit()

                return {"message": "Data saved successfully."}
        finally:
            connection.close()

    except Exception as e:
        error_message = f"Error during processing: {str(e)}"
        print(f"Error: {error_message}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_message)

# FastAPI route to handle voice authentication via HTTP POST
@router.post("/api/voice-auth/login")
async def login(
    password: str = Form(...),
    voice_input: UploadFile = File(...)
):
    try:
        # Step 1: Process the new voice input and generate MFCC vector
        with NamedTemporaryFile(delete=True, suffix=".wav") as temp_file:
            contents = await voice_input.read()
            temp_file.write(contents)
            temp_file.flush()

            # Process new voice input
            new_voice_vector = process_voice(temp_file.name)

        # Step 2: Retrieve the stored MFCC vectors for the given password
        connection = get_singlestore_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT voice_hash_1, voice_hash_2, voice_hash_3 FROM users WHERE password = %s
                """
                cursor.execute(sql, (password,))
                result = cursor.fetchone()

                if not result:
                    raise HTTPException(status_code=401, detail="Invalid credentials")

                stored_vectors = [
                    np.array(json.loads(result['voice_hash_1'])),
                    np.array(json.loads(result['voice_hash_2'])),
                    np.array(json.loads(result['voice_hash_3']))
                ]
        finally:
            connection.close()

        # Step 3: Compare the new MFCC vector with the stored ones using cosine similarity
        for stored_vector in stored_vectors:
            similarity_score = cosine_similarity(new_voice_vector, stored_vector)
            print(f"Similarity Score: {similarity_score}")

            # If similarity is above a certain threshold, authentication is successful
            if similarity_score >= 0.30:  # Adjust threshold as needed
                return {"message": "Authentication successful"}

        return {"message": "Authentication failed"}

    except Exception as e:
        error_message = f"Error during processing: {str(e)}"
        print(f"Error: {error_message}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_message)
