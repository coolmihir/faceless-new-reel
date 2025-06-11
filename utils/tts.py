import os
import requests

def elevenlabs_tts(script, api_key, voice_id, filename):
    output_path = os.path.join("static/outputs", filename)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # good to fail fast if error

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
