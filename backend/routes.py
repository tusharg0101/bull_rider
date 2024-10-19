import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.deepgram import transcribe_audio, generate_speech
from services.groq import generate_tutorial
import logging

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

ROOT_DIR = os.path.abspath(os.curdir) 
TEMP_AUDIO_DIR = os.path.join("/" + ROOT_DIR.strip('/backend'), "temp_audio")  


# Define a pydantic model to validate incoming requests
class TutorialRequest(BaseModel):
    audio_file_path: str
    image_file_path: str

@router.post("/tutorial")
async def tutorial(request: TutorialRequest):
    audio_file_path = request.audio_file_path
    image_file_path = request.image_file_path

    logger.info(f"Received audio file path: {audio_file_path}, image file path: {image_file_path}")
    try:
        # Check if files exist at the given paths
        if not os.path.exists(audio_file_path) or not os.path.exists(image_file_path):
            raise HTTPException(status_code=400, detail="File not found.")

        logger.debug(f"Using audio file at: {audio_file_path}")
        logger.debug(f"Using image file at: {image_file_path}")

        # STEP 2: Transcribe the audio
        logger.debug(f"Attempting to transcribe audio from: {audio_file_path}")
        transcript = transcribe_audio(audio_file_path)
        logger.info(f"Audio transcription successful. Transcript: {transcript[:100]}...")

        # STEP 3: Generate the tutorial
        logger.debug("Generating tutorial based on transcript and image")
        tutorial = generate_tutorial(transcript, image_file_path)
        logger.info(f"Tutorial generation successful. Tutorial: {tutorial[:100]}...")

        # STEP 4: Generate the speech
        logger.debug("Generating speech from tutorial")
        audio_file_name = generate_speech(tutorial)
        logger.info(f"Speech generation successful. Audio file: {audio_file_name}")

        return {"message": "Tutorial received", "audio_file": audio_file_name}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
