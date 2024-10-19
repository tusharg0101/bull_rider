import os
import groq
import base64
from dotenv import load_dotenv
import logging
from typing import List
import asyncio
from services.deepgram import generate_speech

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
logger = logging.getLogger(__name__)

def generate_tutorial(transcript: str, image_file_path: str) -> List[str]:
    groq_client = groq.Client(api_key=GROQ_API_KEY)

    with open(image_file_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Look at an image of the user's screen. Consider the problem they are facing: {transcript}. Come up with simple, easy to follow, numbered steps that the user can follow to achieve their goal. Do not include any other text. Only return the steps. At the end of each step, include a codeword 'END_STEP' so I can split the steps later."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )

    groq_response = chat_completion.choices[0].message.content
    logger.info(f"Groq response: {groq_response}")
    
    # Split the response into steps
    steps = [step.strip() for step in groq_response.split('END_STEP') if step.strip()]
    
    return steps