import requests

def elevenlabs_tts(script, api_key, voice_id, task_id):
    output_path = f"static/outputs/{task_id}.mp3"
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
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path
