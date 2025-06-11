import os
from utils import script_gen, tts, stock_video, merger, captions

def process_video(topic, pexels_api_key, elevenlabs_api_key, voice_id, output_path):
    try:
        os.makedirs("static/outputs", exist_ok=True)

        script = script_gen.generate_script(topic)
        audio = tts.elevenlabs_tts(script, elevenlabs_api_key, voice_id)
        video = stock_video.download_video(topic, pexels_api_key)
        text = captions.transcribe(audio)

        merger.merge(video, audio, text, output_path)

    except Exception as e:
        raise RuntimeError(f"Video generation failed: {e}")
