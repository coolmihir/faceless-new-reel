import os
import requests

def download_video(topic, pexels_api_key, filename):
    output_path = os.path.join("static/outputs", filename)

    headers = {
        "Authorization": pexels_api_key
    }

    response = requests.get(
        f"https://api.pexels.com/videos/search?query={topic}&per_page=1",
        headers=headers
    )
    response.raise_for_status()

    videos = response.json().get("videos")
    if not videos:
        raise Exception("No videos found for the topic.")

    video_url = videos[0]["video_files"][0]["link"]
    video_data = requests.get(video_url)
    video_data.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(video_data.content)

    return output_path
