from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from auth import auth_engine

load_dotenv()

app = FastAPI(title="JARVIS Backend API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Command(BaseModel):
    text: str
    image: str = None  # Optional base64 image data from camera


@app.get("/")
async def root():
    return {"status": "online", "message": "JARVIS Nerve Center is active."}

from brain_engine import brain

@app.post("/api/command")
async def process_command(cmd: Command):
    print(f"Received command: {cmd.text}")
    
    # Check if user wants to create a license
    if "create license" in cmd.text.lower() or "generate key" in cmd.text.lower():
        result = auth_engine.create_license()
        return {
            "response": result.get("message", "License task processed."),
            "data": result,
            "emotion": "smiling"
        }

    # Call the Brain Engine for reasoning and tools
    result = await brain.reason(cmd.text, cmd.image)
    return result



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
