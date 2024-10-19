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
                        # "text": f"Analyze the image of the user's screen. Based on the problem described: {transcript}, provide a clear, step-by-step solution that the user can easily follow to resolve the issue. Ensure the instructions are numbered, concise, and tailored to the user's current screen setup. Focus on making the solution simple and actionable, while avoiding any unnecessary technical jargon."
                        "text": f"Analyze the image of the user's screen. Based on the problem described: {transcript}, provide a set of concise step that the user can follow from where they are in the image to resolve the issue. Use the image, where should i go from what's on my screen. Keep the response to one line."
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