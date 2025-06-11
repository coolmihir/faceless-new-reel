from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os

from video_generator import process_video

app = FastAPI()

# Serve static files (optional, useful if you still want to test locally)
app.mount("/static", StaticFiles(directory="static"), name="static")
os.makedirs("static/outputs", exist_ok=True)

class GenerationRequest(BaseModel):
    topic: str
    pexels_api_key: str
    elevenlabs_api_key: str
    voice_id: str

@app.post("/generate")
async def generate_video(request: GenerationRequest):
    try:
        task_id = str(uuid.uuid4())
        output_path = f"static/outputs/{task_id}.mp4"

        # Generate video
        process_video(
            topic=request.topic,
            pexels_api_key=request.pexels_api_key,
            elevenlabs_api_key=request.elevenlabs_api_key,
            voice_id=request.voice_id,
            output_path=output_path,
            task_id=task_id
        )

        # Return Cloudflare R2 video URL
        video_url = f"https://{os.getenv('R2_PUBLIC_BUCKET_URL')}/{task_id}.mp4"
        return {"video_url": video_url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
