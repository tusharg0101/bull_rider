import os
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from services.deepgram import transcribe_audio, generate_speech
from services.groq import generate_tutorial
from services.db import store_audio, get_audio, get_total_steps, clear_audio, init_db
import logging
from dotenv import load_dotenv
import asyncio

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

@router.on_event("startup")
async def startup_event():
    await init_db()

@router.post("/tutorial")
async def tutorial(
    audio_file_path: str,
    image_file_path: str
):
    load_dotenv()
    tutorial_active = os.getenv('TUTORIAL_ACTIVE', 'FALSE')
    
    try:
        if tutorial_active == "FALSE":
            if not audio_file_path or not image_file_path:
                raise HTTPException(status_code=400, detail="Both audio and image file paths are required for a new tutorial")

            logger.info(f"Received audio file path: {audio_file_path}, image file path: {image_file_path}")

            # Check if files exist
            if not os.path.exists(audio_file_path) or not os.path.exists(image_file_path):
                raise HTTPException(status_code=400, detail="One or both of the specified files do not exist")

            # Transcribe the audio
            transcript = transcribe_audio(audio_file_path)
            logger.info(f"Audio transcription successful. Transcript: {transcript[:100]}...")

            # Generate the tutorial
            steps = generate_tutorial(transcript, image_file_path)
            logger.info(f"Tutorial generation successful. Number of steps: {len(steps)}")

            # Generate and store audio for all steps asynchronously
            async def store_all_audio():
                for i, step in enumerate(steps, start=1):
                    audio_file = generate_speech(step, i)
                    await store_audio(i, audio_file)
                    logger.info(f"Generated and stored audio for step {i}")

            asyncio.create_task(store_all_audio())

            os.environ['TUTORIAL_ACTIVE'] = 'TRUE'
            os.environ['CURRENT_STEP'] = '1'

            # Return the first step's audio
            first_step_audio = generate_speech(steps[0], 0)
            return {
                "step_number": 1,
                "audio_file": first_step_audio,
                "is_last_step": len(steps) == 1
            }
        
        else:
            # This is a subsequent call, get the next step
            current_step = int(os.getenv('CURRENT_STEP', '0'))
            next_step = current_step + 1
            total_steps = await get_total_steps()

            if next_step <= total_steps:
                audio_file = await get_audio(next_step)
                os.environ['CURRENT_STEP'] = str(next_step)
                
                if next_step == total_steps:
                    os.environ['TUTORIAL_ACTIVE'] = 'FALSE'
                    os.environ['CURRENT_STEP'] = '0'
                    asyncio.create_task(clear_audio())

                return {
                    "step_number": next_step,
                    "audio_file": audio_file,
                    "is_last_step": next_step == total_steps
                }
            else:
                os.environ['TUTORIAL_ACTIVE'] = 'FALSE'
                os.environ['CURRENT_STEP'] = '0'
                asyncio.create_task(clear_audio())
                raise HTTPException(status_code=404, detail="No more steps available")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
