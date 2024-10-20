import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router  # Main routes
from services.voice_auth import router as voice_auth_router  # Voice auth routes
import uvicorn

app = FastAPI()

# Add CORS middleware to allow localhost requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)
app.include_router(voice_auth_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8084, reload=True)
