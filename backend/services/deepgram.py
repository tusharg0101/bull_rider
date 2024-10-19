# Test function to make real API calls
import os
import requests
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
    SpeakOptions
)
import json
import logging

# Load environment variables from .env file
load_dotenv()

# Use environment variables

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

def transcribe_audio(audio_file_path):
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        print("i am here")

        with open(audio_file_path, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # json_response = json.loads(response)  # Decode the JSON if it's a string
        return response['results']['channels'][0]['alternatives'][0]['transcript']
    # Function to generate speech
def generate_speech(text, step_number):
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        logging.info(f"Generating speech for text: {text}")

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )
        SPEAK_OPTIONS = {"text": f"{text}"}
        filename = f"output_{step_number}.wav"

        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        logging.info(f"Speech generation successful. Audio file: {filename}")
        return filename

