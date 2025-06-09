from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from video_generator import process_video
import uuid
import os

app = FastAPI()
status_tracker = {}

class RequestBody(BaseModel):
    topic: str
    elevenlabs_api_key: str
    voice_id: str
    pexels_api_key: str

@app.post("/generate")
def generate_reel(data: RequestBody, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    status_tracker[task_id] = "Starting..."
    background_tasks.add_task(process_video, data, task_id, status_tracker)
    return {"task_id": task_id}

@app.get("/status/{task_id}")
def check_status(task_id: str):
    return {"status": status_tracker.get(task_id, "Invalid Task ID")}

@app.get("/result/{task_id}")
def get_result(task_id: str):
    final_path = f"static/outputs/{task_id}.mp4"
    if os.path.exists(final_path):
        return {"video_url": f"/{final_path}"}
    raise HTTPException(status_code=404, detail="Video not ready")
