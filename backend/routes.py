from fastapi import APIRouter, File, UploadFile, Form, Query, HTTPException
from services.deepgram import transcribe_audio, generate_speech
from services.groq import generate_tutorial
import logging
import os

# Set up logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_directory}/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/tutorial")
async def tutorial(audio_file_path: str = Query(...), image_file_path: str = Query(...)):
    logger.info(f"Received request with audio_file_path: {audio_file_path}, image_file_path: {image_file_path}")
    try:
        # STEP 1: Transcribe the audio
        logger.debug(f"Attempting to transcribe audio from: {audio_file_path}")
        transcript = transcribe_audio(audio_file_path)
        logger.info(f"Audio transcription successful. Transcript: {transcript[:100]}...")  # Log first 100 chars

        # STEP 2: Generate the tutorial
        logger.debug("Generating tutorial based on transcript and image")
        tutorial = generate_tutorial(transcript, image_file_path)
        logger.info(f"Tutorial generation successful. Tutorial: {tutorial[:100]}...")  # Log first 100 chars

        # STEP 3: Generate the speech
        logger.debug("Generating speech from tutorial")
        audio_file_name = generate_speech(tutorial)
        logger.info(f"Speech generation successful. Audio file: {audio_file_name}")

        return {"message": "Tutorial received", "audio_file": audio_file_name}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
