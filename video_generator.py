import os
from utils import script_gen, tts, stock_video, merger, captions

def process_video(topic, pexels_api_key, elevenlabs_api_key, voice_id, output_path):
    try:
        print("[1] Generating script...")
        script = script_gen.generate_script(topic)

        print("[2] Generating voiceover...")
        audio_filename = os.path.splitext(os.path.basename(output_path))[0] + ".mp3"
        audio_path = tts.elevenlabs_tts(script, elevenlabs_api_key, voice_id, audio_filename)

        print("[3] Fetching stock video...")
        video_filename = os.path.splitext(os.path.basename(output_path))[0] + ".mp4"
        video_path = stock_video.download_video(topic, pexels_api_key, video_filename)

        print("[4] Generating captions...")
        caption_text = captions.transcribe(audio_path)

        print("[5] Merging video, audio and captions...")
        merger.merge(video_path, audio_path, caption_text, output_path)

        print(f"[✅] Done. Video saved at {output_path}")

    except Exception as e:
        print(f"[❌] Failed: {str(e)}")
        raise
