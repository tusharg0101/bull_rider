import os
import groq
import json
from dotenv import load_dotenv
import base64
import logging
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def generate_tutorial(transcript: str, image_file_path: str):
    groq_client = groq.Client(api_key=GROQ_API_KEY)

    with open(image_file_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # todo: make the prompt better
    # Make Groq API call
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Look at an image of the user's screen. Consider the problem they are facing: {transcript}. Come up with simple, easy to follow, numbered steps that the user can follow to achieve their goal."
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
                "content": f"From the following transcript, extract the task, recipient address, and amount: {transcript}"
            }
        ],
        model="llama-3.2-11b"
    )

    groq_response = chat_completion.choices[0].message.content
    logging.info(f"Transcript: {transcript}")
    logging.info(f"Groq response: {groq_response}")
    return groq_response  # Should be something like: {"task": "send", "address": "0x...", "amount": 100}
    