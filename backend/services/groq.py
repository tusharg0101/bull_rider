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
                        "text": f"Analyze the image of the user's screen. Based on the problem described by the user: {transcript}, provide a clear, step-by-step solution that the user can easily follow to resolve the issue. Ensure the instructions are numbered, concise, and tailored to the user's current screen setup. Focus on making the solution simple and actionable, while avoiding any unnecessary technical jargon. Do not include any other text. Only return the steps. At the end of each step, include a codeword 'END_STEP' so I can split the steps later."
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
    logging.info(f"Groq response: {groq_response}")
    return groq_response

    

def parse_transaction(transcript: str):
    groq_client = groq.Client(api_key=GROQ_API_KEY)

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"From the following {transcript}, extract the recipient's name (which is typically a person's name), and the amount of tokens. If you encounter the words 'token', 'tokens', 'coin', or 'coins', they all mean the same thing. Additionally, convert any alphanumeric characters such as 'one', 'two', 'three', etc., into their respective numbers. Ensure that the amount is an integer and appears at the very end of the response. Format the response in the following way: 'Recipient: [recipient's name], Amount: [amount]'. Don't include any ' in the response. The amount must be the last character of the response so that it can be easily extracted by accessing the last character of the response."
            }
        ],
        model="llama-3.2-11b-vision-preview"
    )

    groq_response = chat_completion.choices[0].message.content
    logging.info(f"Transcript: {transcript}")
    logging.info(f"Groq response: {groq_response}")
    return groq_response  # Should be something like: {"task": "send", "address": "0x...", "amount": 100}
    
