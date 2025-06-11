from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os
from video_generator import process_video

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure output directory exists
os.makedirs("static/outputs", exist_ok=True)

# Request model
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

        process_video(
            topic=request.topic,
            pexels_api_key=request.pexels_api_key,
            elevenlabs_api_key=request.elevenlabs_api_key,
            voice_id=request.voice_id,
            output_path=output_path
        )

        return {"video_url": f"/{output_path}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
