import whisper
import sounddevice as sd
import numpy as np
import tempfile
import wave
from config import DEBUG


def record_audio(duration: float, samplerate: int = 16000) -> bytes:
    """
    Record audio from the microphone for a specified duration.

    Returns:
        bytes: Recorded audio in WAV format.
    """
    if DEBUG:
        print(f"[DEBUG] Recording audio for {duration} seconds...")

    # Record audio data
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()

    # Convert recorded data to bytes in WAV format
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        with wave.open(tmp_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit samples
            wf.setframerate(samplerate)
            # Convert float32 to int16 for WAV
            wf.writeframes((audio_data * np.iinfo(np.int16).max).astype(np.int16).tobytes())
        tmp_file.seek(0)
        audio_bytes = tmp_file.read()

    if DEBUG:
        print("[DEBUG] Recording complete.")
    return audio_bytes


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe given WAV audio bytes using Whisper.

    Returns:
        str: Transcribed text.
    """
    # Load Whisper model (select model size based on desired accuracy/speed)
    model = whisper.load_model("base.en")  # Use "base" or "tiny" for faster but less accurate results

    # Save audio_bytes to a temporary file for transcription
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file.flush()
        result = model.transcribe(tmp_file.name)

    transcript = result["text"]
    if DEBUG:
        print(f"[DEBUG] Transcribed text: {transcript}")
    return transcript


def record_and_transcribe(duration: float = 5.0) -> str:
    """
    Record audio for a specified duration and return the transcribed text.

    Args:
        duration (float): Duration in seconds to record.

    Returns:
        str: Transcribed text.
    """
    audio_bytes = record_audio(duration)
    return transcribe_audio(audio_bytes)