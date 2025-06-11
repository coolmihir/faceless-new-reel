from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

def merge(video_path, audio_path, text, output_path):
    # Load and downscale video to reduce memory footprint
    video = VideoFileClip(video_path).resize(height=720)  # Maintain aspect ratio, reduce height

    # Load audio
    audio = AudioFileClip(audio_path)

    # Create text overlay
    text_clip = TextClip(
        text,
        fontsize=40,
        color='white',
        bg_color='black',
        size=(video.w, 100)
    ).set_duration(video.duration).set_position(("center", "bottom"))

    # Combine everything
    final_clip = CompositeVideoClip([video, text_clip])
    final_clip = final_clip.set_audio(audio)

    # Write final video with optimized settings for low-resource environments
    final_clip.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        preset='ultrafast',
        threads=1,
        logger=None  # Suppress verbose logging
    )
