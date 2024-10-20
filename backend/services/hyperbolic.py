import os
from dotenv import load_dotenv
import logging
from typing import List
import base64
import requests
from io import BytesIO
from PIL import Image
from services.scrape_and_rag import retrieve_context

logger = logging.getLogger(__name__)

load_dotenv()

HYPERBOLIC_API_KEY = os.getenv('HYPERBOLIC_API_KEY')

def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string

def generate_tutorial(transcript: str, image_file_path: str) -> List[str]:
    relevant_context = retrieve_context(transcript)
    
    if not relevant_context:
        logger.warning("No relevant context found. Proceeding without context.")
        context = "No specific context available."
    else:
        context = "\n".join(relevant_context)

    prompt = f"""Analyze the image of the user's screen. 
    Based on the problem described by the user: {transcript}, 
    and considering this context: {context},
    provide a clear, step-by-step solution that the user can easily follow to resolve the issue. 
    Ensure the instructions are numbered, concise, and tailored to the user's current screen setup. 
    Focus on making the solution simple and actionable, while avoiding any unnecessary technical jargon. 
    Do not include any other text. Only return the steps. At the end of each step and before the next step, include a codeword 'END_STEP' 
    so I can split the steps later."""
        
    img = Image.open(image_file_path)
    base64_img = encode_image(img)

    api = "https://api.hyperbolic.xyz/v1/chat/completions"
    api_key = os.getenv("HYPERBOLIC_API_KEY")

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
    hyperbolic_response = response.json()['choices'][0]['message']['content']
    steps = [step.strip() for step in hyperbolic_response.split('END_STEP') if step.strip()]
    return steps