import os
from utils import script_gen, tts, stock_video, merger, captions

def process_video(topic, pexels_api_key, elevenlabs_api_key, voice_id, output_path):
    try:
        # Create output directory if it doesn't exist
        os.makedirs("static/outputs", exist_ok=True)

        # Step 1: Generate script
        script = script_gen.generate_script(topic)

        # Step 2: Generate voiceover
        audio_path = tts.elevenlabs_tts(script, elevenlabs_api_key, voice_id, "temp_audio")

        # Step 3: Fetch relevant stock video
        video_path = stock_video.download_video(topic, pexels_api_key, "temp_video")

        # Step 4: Generate captions from voiceover
        captions_text = captions.transcribe(audio_path)

        # Step 5: Merge everything into a vertical reel
        merger.merge(video_path, audio_path, captions_text, output_path)

    except Exception as e:
        raise RuntimeError(f"Video generation failed: {e}")
