import os
import groq
import base64
from dotenv import load_dotenv
import logging
from typing import List
import asyncio
from services.deepgram import generate_speech

# load_dotenv()

# GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# logger = logging.getLogger(__name__)

# def generate_tutorial(transcript: str, image_file_path: str) -> List[str]:
#     groq_client = groq.Client(api_key=GROQ_API_KEY)

#     with open(image_file_path, "rb") as image_file:
#         base64_image = base64.b64encode(image_file.read()).decode('utf-8')

#     chat_completion = groq_client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": f"Analyze the image of the user's screen. Based on the problem described by the user: {transcript}, provide a clear, step-by-step solution that the user can easily follow to resolve the issue. Ensure the instructions are numbered, concise, and tailored to the user's current screen setup. Focus on making the solution simple and actionable, while avoiding any unnecessary technical jargon. Do not include any other text. Only return the steps. At the end of each step, include a codeword 'END_STEP' so I can split the steps later."
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}",
#                         },
#                     },
#                 ],
#             }
#         ],
#         model="llama-3.2-90b-vision-preview",
#     )

#     groq_response = chat_completion.choices[0].message.content
    
#     # Split the response into steps
#     steps = [step.strip() for step in groq_response.split('END_STEP') if step.strip()]
    
#     return steps

import base64
import requests
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)


def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string

def generate_tutorial(transcript: str, image_file_path: str) -> List[str]:

    prompt = f"""Analyze the image of the user's screen. 
    Based on the problem described by the user: {transcript}, 
    provide a clear, step-by-step solution that the user can easily follow to resolve the issue. 
    Ensure the instructions are numbered, concise, and tailored to the user's current screen setup. 
    Focus on making the solution simple and actionable, while avoiding any unnecessary technical jargon. 
    Do not include any other text. Only return the steps. At the end of each step, include a codeword 'END_STEP' 
    so I can split the steps later."""

    logger.info(f"tushi Prompt: {prompt}")
        
    img = Image.open(image_file_path)
    base64_img = encode_image(img)

    api = "https://api.hyperbolic.xyz/v1/chat/completions"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0dXNoYXJnMDEwMUBnbWFpbC5jb20iLCJpYXQiOjE3Mjk0MDIxMzh9.utW7QvizgBfY9Idz6HtTDVsFK72tEvTS6Th-CIa7l7o"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                    },
                ],
            }
        ],
        "model": "mistralai/Pixtral-12B-2409",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    response = requests.post(api, headers=headers, json=payload)
    logger.info(f"tushi Hyperbolic response: {response.json()}")
    return response.json()['choices'][0]['message']['content']

