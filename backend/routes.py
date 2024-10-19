import os
from fastapi import APIRouter, File, UploadFile, HTTPException
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

@router.post("/tutorial")
async def tutorial(audio_file: UploadFile = File(...), image_file: UploadFile = File(...)):
    logger.info(f"Received audio file: {audio_file.filename}, image file: {image_file.filename}")
    try:
        # STEP 1: Define full paths for audio and image files in `temp_audio`
        audio_file_path = os.path.join(TEMP_AUDIO_DIR, audio_file.filename)
        image_file_path = os.path.join(TEMP_AUDIO_DIR, image_file.filename)

        logger.debug(f"Saving audio to: {audio_file_path}")
        logger.debug(f"Saving image to: {image_file_path}")

        # Save the audio and image files
        with open(audio_file_path, "wb") as audio_out:
            audio_out.write(await audio_file.read())

        with open(image_file_path, "wb") as image_out:
            image_out.write(await image_file.read())

        logger.info(f"Files saved: {audio_file_path}, {image_file_path}")

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
