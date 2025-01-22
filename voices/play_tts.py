from elevenlabs import play
from tts import synthesize_speech, DEBUG

if DEBUG:
    print("[DEBUG] Running play_tts.py - Direct Speaker Playback Test")


def main():
    # Prompt user for input text
    text = input("Enter text to synthesize and play: ")

    if DEBUG:
        print(f"[DEBUG] Synthesizing for text: {text}")

    try:
        # Synthesize speech from the input text
        audio_data = synthesize_speech(text)

        if DEBUG:
            print("[DEBUG] Synthesized speech successfully. Playing audio...")

        # Play the synthesized audio through speakers
        play(audio_data)

        if DEBUG:
            print("[DEBUG] Playback finished.")

        print("Audio playback complete.")

    except Exception as e:
        print(f"Error during synthesis or playback: {e}")


if __name__ == "__main__":
    main()