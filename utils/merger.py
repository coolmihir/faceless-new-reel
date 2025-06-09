from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

def merge(video_path, audio_path, text, output_path):
    video = VideoFileClip(video_path).resize((720, 1280))
    audio = AudioFileClip(audio_path)

    text_clip = TextClip(
        text,
        fontsize=40,
        color='white',
        bg_color='black',
        size=(video.w, 100)
    ).set_duration(video.duration).set_position(("center", "bottom"))

    final_clip = CompositeVideoClip([video, text_clip])
    final_clip = final_clip.set_audio(audio)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
