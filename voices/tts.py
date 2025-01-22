# tts.py
from elevenlabs import ElevenLabs
from config import DEBUG, ELEVENLABS_API_KEY, ELEVENLABS_MODEL_ID, ELEVENLABS_OUTPUT_FORMAT, ELEVENLABS_VOICE_ID

# Initialize ElevenLabs client with provided configuration
if DEBUG:
    print(f"[DEBUG] Initializing ElevenLabs client with the following settings:")
    print(f"        Voice ID: {ELEVENLABS_VOICE_ID}")
    print(f"        Model ID: {ELEVENLABS_MODEL_ID}")
    print(f"        Output Format: {ELEVENLABS_OUTPUT_FORMAT}")

# Create a single instance of ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def synthesize_speech(text: str) -> bytes:
    """
    Convert the provided text into speech using ElevenLabs TTS.

    Args:
        text (str): The text to be converted into speech.

    Returns:
        bytes: The synthesized audio content in the format specified in the configuration.

    Raises:
        Exception: Propagates any exception encountered during the API call.
    """
    if DEBUG:
        print(f"[DEBUG] Synthesizing speech for the text: {text}")
        print(f"        Using Voice ID: {ELEVENLABS_VOICE_ID}")
        print(f"        Using Model ID: {ELEVENLABS_MODEL_ID}")
        print(f"        Output Format: {ELEVENLABS_OUTPUT_FORMAT}")

    try:
        # Call ElevenLabs TTS API to convert text to speech
        audio_content = client.text_to_speech.convert(
            voice_id=ELEVENLABS_VOICE_ID,
            output_format=ELEVENLABS_OUTPUT_FORMAT,
            text=text,
            model_id=ELEVENLABS_MODEL_ID,
        )

        if DEBUG:
            print("[DEBUG] Speech synthesis successful. Received audio content.")

        return audio_content

    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error during speech synthesis: {e}")
        # Reraise the exception after logging
        raise