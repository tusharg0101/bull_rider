import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.deepgram import transcribe_audio, generate_speech
from services.groq import generate_tutorial, parse_transaction
from services.sui import get_sui_client, send_transaction
from services.db import store_audio, get_audio, get_total_steps, clear_audio, init_db, init_name_address, get_address_from_name, set_name_address
import logging
from dotenv import load_dotenv
import asyncio
import json
from services.scrape_and_rag import init_rag

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

class TutorialStateRequest(BaseModel):
	state: bool

class CurrentStepRequest(BaseModel):
	step: int

@router.on_event("startup")
async def startup_event():
	await init_db()
	await init_rag()  # This should now work correctly
	await init_name_address()
	

# Global variables to store the tutorial state and current step
tutorial_active = False
current_step = 0

@router.get("/tutorial_state")
async def get_tutorial_state():
	return {"tutorial_active": tutorial_active}

@router.post("/tutorial_state")
async def set_tutorial_state(request: TutorialStateRequest):
	global tutorial_active
	tutorial_active = request.state
	return {"tutorial_active": tutorial_active}

@router.get("/current_step")
async def get_current_step():
	return {"current_step": current_step}

@router.post("/current_step")
async def set_current_step(request: CurrentStepRequest):
	global current_step
	current_step = request.step
	return {"current_step": current_step}

@router.post("/tutorial")
async def tutorial(request: TutorialRequest):
	global tutorial_active, current_step
	audio_file_path = request.audio_file_path
	image_file_path = request.image_file_path

	logger.info(f"tutorial_active: {tutorial_active}, current_step: {current_step}")
	logger.info(f"Received audio file path: {audio_file_path}, image file path: {image_file_path}")

	try:
		if tutorial_active == True:
    
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
				for i, step in enumerate(steps[1:], start=1):
					audio_file = generate_speech(step, i)
					await store_audio(i, audio_file)
					logger.info(f"Generated and stored audio for step {i}")

			tutorial_active = False
			current_step = 0

			# Return the first step's audio
			first_step_audio = generate_speech(steps[0], 0)
			asyncio.create_task(store_all_audio())
		
			return {
				"step_number": 0,
				"audio_file": first_step_audio,
				"is_last_step": len(steps) == 1
			}
		
		else:
			# This is a subsequent call, get the next step
			next_step = current_step + 1
			total_steps = await get_total_steps()

			logger.info(f"Current step: {current_step}, Next step: {next_step}, Total steps: {total_steps}")

			if next_step <= total_steps:
				audio_file = await get_audio(next_step)
				current_step = next_step
				
				if next_step == total_steps:
					tutorial_active = False
					current_step = 0
					await clear_audio()

				return {
					"step_number": next_step,
					"audio_file": audio_file,
					"is_last_step": next_step == total_steps
				}
			else:
				tutorial_active = False
				current_step = 0
				await clear_audio()

	except Exception as e:
		logger.error(f"An error occurred: {str(e)}", exc_info=True)
		raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/initiate-transaction")
async def initiate_transaction(audio_file_path: str):
    logger.info("Received transaction request")
    
    try:
        # Step 1: Transcribe the audio
        logger.debug(f"Transcribing audio from file: {audio_file_path}")
        transcript = transcribe_audio(audio_file_path)
        logger.info(f"Transcription successful: {transcript[:100]}...")  # Log first 100 chars
        
        # Step 2: Parse the transcript for task details (recipient, amount)
        logger.debug("Parsing transcript for transaction details")
        transaction_details = parse_transaction(transcript)
        #transaction_details = json.loads(transaction_details)
        logger.info(f"Transaction details parsed: {transaction_details}")
        
        # Extract recipient and amount
        #recipient_name = transaction_details['address']
        #recipient_address = await get_address_from_name(recipient_name)   
        logger.info(f"Transaction details String: {transaction_details[-1]}")
        logger.info(f"Transaction details Integer: {int(transaction_details[-1])}")
        amount = int(transaction_details[-1]) * 1000000000 # Convert to Sui units

        # Step 3: Execute the transaction on Sui
        logger.debug(f"Executing transaction on Sui: sending {amount} to {recipient_address}")
        client = await get_sui_client()
        #logger.debug(f"address of client{client['config']['addresses']}")
        logger.info("Got client")
        transaction_digest = await send_transaction(client, recipient_address, amount)
        logger.info(f"Transaction successful: {transaction_digest}")

        return {"message": "Transaction initiated", "transaction_digest": transaction_digest}
    
    except Exception as e:
        logger.error(f"Error during transaction initiation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Transaction initiation failed: {str(e)}")
