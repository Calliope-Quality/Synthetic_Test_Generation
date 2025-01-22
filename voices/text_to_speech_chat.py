from ai_response import get_ai_response
from tts import synthesize_speech, DEBUG
from elevenlabs import play

def process_text_query(user_input: str) -> str:
    """
    Process a text query: send it to the AI, synthesize the response, and play audio.

    Args:
        user_input (str): The user's text input.

    Returns:
        str: The AI's text response.
    """
    # Get AI response based on user input
    ai_text = get_ai_response(user_input)

    if DEBUG:
        print(f"[DEBUG] AI Text Response: {ai_text}")

    # Synthesize the AI response into speech
    audio_data = synthesize_speech(ai_text)

    if DEBUG:
        print("[DEBUG] Playing synthesized speech...")

    # Play the synthesized speech
    play(audio_data)

    return ai_text


def main():
    print("Welcome to the text-to-AI-to-speech interface. Type 'exit' to quit.")
    while True:
        user_input = input("Enter your prompt: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Process the text query and retrieve the AI response
        process_text_query(user_input)


if __name__ == "__main__":
    main()