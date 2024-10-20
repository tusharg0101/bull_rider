from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import librosa
import hashlib
import numpy as np
from tempfile import NamedTemporaryFile
from .singlestore_project1 import get_singlestore_connection
router = APIRouter()

# Helper function to process the audio file and return its hash
def process_voice(file_path: str) -> str:
    y, sr = librosa.load(file_path, sr=None)  # Load with original sample rate
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    flat_mfcc = mfcc.flatten()
    
    # Hash the MFCCs for authentication
    voice_hash = hashlib.sha256(flat_mfcc.tobytes()).hexdigest()
    return voice_hash

# FastAPI route to handle voice auth
@router.post("/api/voice-auth")
async def voice_auth(
    password: str = Form(...),
    audio_1: UploadFile = File(...),
    audio_2: UploadFile = File(...),
    audio_3: UploadFile = File(...)
):
    audio_files = [audio_1, audio_2, audio_3]
    voice_hashes = []

    # Process each uploaded file
    for audio in audio_files:
        # Use a temporary file to store the uploaded audio before processing
        with NamedTemporaryFile(delete=True, suffix=".wav") as temp_file:
            temp_file.write(await audio.read())  # Write the audio byte stream to the temp file
            temp_file.flush()  # Ensure all data is written
            # Process the voice and generate a hash
            voice_hash = process_voice(temp_file.name)
            voice_hashes.append(voice_hash)

    # Store the password and voice hashes in SingleStore
    connection = get_singlestore_connection()
    try:
        with connection.cursor() as cursor:
            # Insert the password and voice hashes into the database
            sql = """
            INSERT INTO users (password, voice_hash_1, voice_hash_2, voice_hash_3)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (password, voice_hashes[0], voice_hashes[1], voice_hashes[2]))
            connection.commit()
    finally:
        connection.close()

    # Return the password and voice hashes
    return {"password": password, "voice_hashes": voice_hashes}
