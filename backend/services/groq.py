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

def parse_transaction(transcript: str):
    groq_client = groq.Client(api_key=GROQ_API_KEY)

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"From the following {transcript}, extract the recipient's name (which is typically a person's name), and the amount of tokens. If you encounter the words 'token', 'tokens', 'coin', or 'coins', they all mean the same thing. Additionally, convert any alphanumeric characters such as 'one', 'two', 'three', etc., into their respective numbers. Ensure that the amount is an integer and appears at the very end of the response. Format the response in the following way: 'Recipient: [recipient's name], Amount: [amount]'. Don't include any ' in the response. The amount must be the last character of the response so that it can be easily extracted by accessing the last character of the response."
            }
        ],
        model="llama-3.2-11b"
    )

    groq_response = chat_completion.choices[0].message.content
    logging.info(f"Transcript: {transcript}")
    logging.info(f"Groq response: {groq_response}")
    return groq_response  # Should be something like: {"task": "send", "address": "0x...", "amount": 100}
    
