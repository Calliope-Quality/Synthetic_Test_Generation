from ai_response import get_ai_response
from tts import synthesize_speech, DEBUG
from stt import record_and_transcribe
from elevenlabs import play


def main():
    print("Voice Chat Mode: Press Enter to speak, or type 'exit' to quit.")
    while True:
        # Wait for user to initiate speaking
        command = input("\nPress Enter to speak (or type 'exit' to quit): ")
        if command.strip().lower() in ["exit", "quit"]:
            print("Exiting voice chat. Goodbye!")
            break

        # Record and transcribe user speech
        print("Recording... Please speak now.")
        user_text = record_and_transcribe(duration=5.0)  # adjust duration as needed

        if DEBUG:
            print(f"[DEBUG] Transcribed user input: {user_text}")

        # Check if transcription indicates a desire to exit
        if user_text.strip().lower() in ["exit", "quit"]:
            print("Exit command recognized. Goodbye!")
            break

        # Get AI response
        ai_text = get_ai_response(user_text)
        print(f"Assistant: {ai_text}")

        # Synthesize and play AI response
        audio_data = synthesize_speech(ai_text)
        play(audio_data)


if __name__ == "__main__":
    main()