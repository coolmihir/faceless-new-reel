from faster_whisper import WhisperModel

def transcribe(audio_path):
    model = WhisperModel("base", compute_type="int8")  # use 'tiny' or 'base' for small size
    segments, _ = model.transcribe(audio_path)
    return " ".join([segment.text for segment in segments])
