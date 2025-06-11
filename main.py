from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os

from video_generator import process_video
from utils.upload_to_r2 import upload_to_r2  # <-- New import for R2

# Initialize FastAPI app
app = FastAPI()

# Serve static files from the "static" directory (optional)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create output directory if it doesn't exist
os.makedirs("static/outputs", exist_ok=True)

# Request model
class GenerationRequest(BaseModel):
    topic: str
    pexels_api_key: str
    elevenlabs_api_key: str
    voice_id: str

# /generate endpoint
@app.post("/generate")
async def generate_video(request: GenerationRequest):
    try:
        # Unique task ID and video output path
        task_id = str(uuid.uuid4())
        output_path = f"static/outputs/{task_id}.mp4"

        # Wrap the data to pass to video generator
        data = request

        # Temporary tracker (optional, you can remove if not using progress tracking)
        status_tracker = {}

        # Process the video (local generation)
        process_video(data, task_id, status_tracker)

        # Upload to Cloudflare R2
        uploaded_url = upload_to_r2(output_path)

        return {"video_url": uploaded_url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
