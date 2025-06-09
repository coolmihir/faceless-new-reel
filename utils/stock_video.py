import requests

def download_video(topic, pexels_api_key, task_id):
    headers = {"Authorization": pexels_api_key}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page=1"
    response = requests.get(url, headers=headers)
    video_url = response.json()['videos'][0]['video_files'][0]['link']

    output_path = f"static/outputs/{task_id}.mp4"
    video_data = requests.get(video_url)
    with open(output_path, "wb") as f:
        f.write(video_data.content)

    return output_path
