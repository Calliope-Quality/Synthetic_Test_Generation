# voice_chat_ado_integration_faiss.py

import re
from dotenv import load_dotenv

# Voice libraries
from stt import record_and_transcribe
from tts import synthesize_speech
from elevenlabs import play
from logger import logger

# AI logic
from ai_response import get_ai_response  # or wherever your get_ai_response is located

# ADO + RAG integration
from modules.ado_integration import get_user_story_from_ado
from modules.user_story_processor import process_user_story
from modules.rag_engine_faiss import generate_test_cases
from modules.test_case_formatter import format_test_cases
from modules.test_case_exporter import parse_test_cases, save_test_cases_to_csv

# Vector DB
from utils.vector_db import initialize_faiss_index

load_dotenv()

def main():
    """
    Combined voice assistant that:
      - Listens for voice commands.
      - If user asks "generate test cases for user story [ID]", we run the test case pipeline.
      - Otherwise, we pass their request to a general AI conversation via get_ai_response.
      - Then respond with TTS.
    """
    print("Voice Chat Mode: Press Enter to speak, or type 'exit' to quit.")

    # Initialize the FAISS index so we can perform retrieval
    initialize_faiss_index(dimension=1536)

    while True:
        command = input("\nPress Enter to speak (or type 'exit' to quit): ")
        if command.strip().lower() in ["exit", "quit"]:
            print("Exiting voice chat. Goodbye!")
            break

        print("Recording... Please speak now.")
        user_text = record_and_transcribe(duration=10.0).strip()
        print(f"You said: {user_text}")

        # Check if user wants to exit by voice
        if user_text.lower() in ["exit", "quit"]:
            print("Exit command recognized. Goodbye!")
            break

        # Check if the user wants to generate test cases for a given user story ID
        if "generate test cases" in user_text.lower() and "user story" in user_text.lower():
            story_id = extract_story_id(user_text)
            if story_id:
                response_text = handle_test_case_generation(story_id)
            else:
                response_text = "I’m sorry, I didn’t catch a valid user story ID in your request."
        else:
            # Not recognized as a test-case command, so let's use our AI fallback
            response_text = get_ai_response(user_text)

        # Print response to terminal
        print(f"Assistant: {response_text}")
        # Synthesize and play TTS response
        try:
            audio_data = synthesize_speech(response_text)
            play(audio_data)
        except Exception as e:
            logger.error(f"Error playing TTS audio: {e}")
            print("Sorry, I had trouble speaking my response.")

def extract_story_id(transcribed_text):
    """
    Attempts to parse a numeric story ID from the user's command.
    Example phrase: "generate test cases for user story 144329"
    Returns the ID (e.g. "144329") or None if not found.
    """
    match = re.search(r"user story\s+(\d+)", transcribed_text.lower())
    return match.group(1) if match else None


def handle_test_case_generation(story_id):
    """
    Orchestrates the ADO -> RAG -> CSV pipeline using a story_id.
    Returns a string to speak back to the user.
    """
    try:
        # 1) Pull user story from ADO
        user_story = get_user_story_from_ado(story_id)
        if not user_story:
            return f"Failed to retrieve user story ID {story_id} from ADO."

        # 2) Process user story (e.g. strip HTML)
        processed_story = process_user_story(user_story)

        # 3) Generate test cases (RAG with FAISS + OpenAI)
        raw_test_cases = generate_test_cases(processed_story)
        if not raw_test_cases:
            return "I’m sorry, I couldn’t generate test cases at this time."

        # 4) Format
        formatted_test_cases = format_test_cases(raw_test_cases)

        # 5) Parse & Save to CSV
        parsed_data = parse_test_cases(formatted_test_cases)
        if not parsed_data:
            return "No test cases were returned from the AI."

        save_test_cases_to_csv(parsed_data, csv_file="my_voice_test_cases.csv")

        return f"Test cases for story {story_id} have been generated and saved to 'my_voice_test_cases.csv'."

    except Exception as e:
        logger.error(f"Error in handle_test_case_generation: {e}")
        return "I encountered an error generating the test cases. Please check the logs."

if __name__ == "__main__":
    main()