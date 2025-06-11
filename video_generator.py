import os
from utils import script_gen, tts, stock_video, merger, captions
import boto3

def process_video(topic, pexels_api_key, elevenlabs_api_key, voice_id, output_path, task_id):
    try:
        # Generate script
        script = script_gen.generate_script(topic)

        # Generate voiceover
        audio_path = tts.elevenlabs_tts(script, elevenlabs_api_key, voice_id, task_id)

        # Download stock video
        video_path = stock_video.download_video(topic, pexels_api_key, task_id)

        # Transcribe to captions
        subtitle_text = captions.transcribe(audio_path)

        # Merge everything into final video
        merger.merge(video_path, audio_path, subtitle_text, output_path)

        # Upload to Cloudflare R2
        upload_to_r2(output_path, f"{task_id}.mp4")

    except Exception as e:
        raise Exception(f"Video generation failed: {str(e)}")

def upload_to_r2(local_path, remote_filename):
    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv("R2_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
    )
    bucket_name = os.getenv("R2_BUCKET_NAME")

    with open(local_path, "rb") as file_data:
        s3.upload_fileobj(file_data, bucket_name, remote_filename)
