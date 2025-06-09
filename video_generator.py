import os
from utils import script_gen, tts, stock_video, merger, captions

def process_video(data, task_id, status_tracker):
    try:
        os.makedirs("static/outputs", exist_ok=True)

        status_tracker[task_id] = "Generating script..."
        script = script_gen.generate_script(data.topic)

        status_tracker[task_id] = "Generating voiceover..."
        audio = tts.elevenlabs_tts(script, data.elevenlabs_api_key, data.voice_id, task_id)

        status_tracker[task_id] = "Fetching video..."
        video = stock_video.download_video(data.topic, data.pexels_api_key, task_id)

        status_tracker[task_id] = "Generating captions..."
        text = captions.transcribe(audio)

        status_tracker[task_id] = "Merging final reel..."
        output_path = f"static/outputs/{task_id}.mp4"
        merger.merge(video, audio, text, output_path)

        status_tracker[task_id] = "Done ✅"
    except Exception as e:
        status_tracker[task_id] = f"Failed ❌: {str(e)}"
