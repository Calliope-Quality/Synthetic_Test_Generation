# voice_chat_ado_integration_chromadb.py

import re
from dotenv import load_dotenv
import logging

# Voice libraries
from stt import record_and_transcribe
from tts import synthesize_speech
from elevenlabs import play

# Logging
from logger import logger

# AI logic
from ai_response import get_ai_response  # or wherever your get_ai_response is located

# ADO + user story logic
from modules.ado_integration import get_user_story_from_ado
from modules.user_story_processor import process_user_story

# === NEW: Import Chroma-based RAG engine instead of FAISS
from modules.rag_engine_chroma import generate_test_cases_chroma  # RAG code

# Test case formatting & exporting
from modules.test_case_formatter import format_test_cases
from modules.test_case_exporter import parse_test_cases, save_test_cases_to_csv

load_dotenv()

# Configure extra debug if needed
logging.basicConfig(level=logging.DEBUG)  # or use your config.py for a global DEBUG

def main():
    """
    Combined voice assistant that:
      - Listens for voice commands.
      - If user asks "generate test cases/test scripts/test data for story [ID]",
        run the test case pipeline (Chroma version) with real ADO data if available.
      - Otherwise, pass request to a general AI conversation via get_ai_response.
      - Then respond with TTS.
    """
    print("Voice Chat Mode: Press Enter to speak, or type 'exit' to quit.")

    while True:
        command = input("\nPress Enter to speak (or type 'exit' to quit): ")
        if command.strip().lower() in ["exit", "quit"]:
            print("Exiting voice chat. Goodbye!")
            break

        logger.debug("Recording user speech for up to 10 seconds...")
        print("Recording... Please speak now.")
        user_text = record_and_transcribe(duration=10.0).strip()
        logger.debug(f"Transcribed speech: '{user_text}'")
        print(f"You said: {user_text}")

        if user_text.lower() in ["exit", "quit"]:
            print("Exit command recognized. Goodbye!")
            break

        # Check if the user wants to generate test cases (or scripts, data, etc.)
        # by matching the new flexible regex
        if user_wants_test_generation(user_text):
            logger.debug("Detected a phrase about generating test cases/scripts/data.")
            story_id = extract_story_id(user_text)
            if story_id:
                logger.debug(f"Extracted story ID: {story_id}. Attempting handle_test_case_generation...")
                response_text = handle_test_case_generation(story_id)
            else:
                logger.debug("Could not extract any numeric story ID from speech.")
                response_text = (
                    "I heard you request test cases or scripts, "
                    "but I didn’t catch a valid user story ID. Please say something like: "
                    "'Generate test cases for user story 12345,' or I'll use a generic approach."
                )
        else:
            logger.debug("No test-generation phrase detected. Using standard AI fallback.")
            response_text = get_ai_response(user_text)

        logger.debug(f"Assistant response before TTS: {response_text}")
        print(f"Assistant: {response_text}")

        try:
            audio_data = synthesize_speech(response_text)
            play(audio_data)
        except Exception as e:
            logger.error(f"Error playing TTS audio: {e}")
            print("Sorry, I had trouble speaking my response.")

def user_wants_test_generation(transcribed_text: str) -> bool:
    """
    Returns True if the user text includes phrases like:
      - "generate test cases"
      - "generate test scripts"
      - "generate test data"
      - "synthetic test cases"
    plus references "story" or "user story" somewhere after that.

    The NEW regex uses (generate).*? to allow optional words (e.g. "generate some test cases")
    before we match test cases/scripts/data, then eventually "story".
    """
    phrase_pattern = (
        r"(generate).*?"
        r"(?:test\s*(?:cases|scripts|data)|synthetic\s*test\s*cases).*?"
        r"(?:story|user\s*story)"
    )
    match_found = bool(re.search(phrase_pattern, transcribed_text.lower()))
    logger.debug(f"user_wants_test_generation? {match_found} for text='{transcribed_text}'")
    return match_found

def extract_story_id(transcribed_text: str):
    """
    Attempts to parse a numeric story ID from the user's command.
    Example phrases:
      - "generate test cases for user story 144329"
      - "I want synthetic test data for story 123"
    Returns the ID (e.g., "144329") or None if not found.
    """
    match = re.search(r"(?:story|user\s*story)\s+(\d+)", transcribed_text.lower())
    found_id = match.group(1) if match else None
    logger.debug(f"extract_story_id found: {found_id} from text='{transcribed_text}'")
    return found_id


def handle_test_case_generation(story_id: str) -> str:
    try:
        logger.debug(f"handle_test_case_generation called with story_id={story_id}")
        # 1) Pull user story from ADO
        user_story = get_user_story_from_ado(story_id)
        if not user_story:
            logger.debug(f"No data returned from get_user_story_from_ado for ID={story_id}")
            return (
                f"I couldn’t find user story {story_id} in ADO. "
                "I'll just create synthetic test cases from your speech context.\n"
                "Is that okay? If so, please say something like 'generate test cases for user story zero' or 'generate test cases without ADO data.'"
            )

        logger.debug(f"Fetched user story from ADO (length={len(user_story)} chars). Processing it now...")
        processed_story = process_user_story(user_story)

        logger.debug("Calling generate_test_cases_chroma with processed story.")
        raw_test_cases = generate_test_cases_chroma(processed_story)
        if not raw_test_cases or raw_test_cases.startswith("ERROR:"):
            logger.debug(f"RAG generation returned error or empty: {raw_test_cases}")
            return (
                "I’m sorry, I couldn’t generate test cases at this time. "
                "Perhaps the data from ADO was insufficient or there's a system issue."
            )

        # Print the raw test cases to terminal
        print("\n--- Raw Test Cases Output ---")
        print(raw_test_cases)
        print("--- End of Raw Test Cases Output ---\n")

        logger.debug("Formatting the AI-generated test cases.")
        # After fetching raw_test_cases and formatting them
        formatted_test_cases = format_test_cases(raw_test_cases)
        logger.debug(f"Formatted test cases: {formatted_test_cases}")

        # Use parse_test_case_block on each formatted block
        from modules.test_case_formatter import parse_test_case_block  # ensure it's imported

        parsed_cases = [parse_test_case_block(block) for block in formatted_test_cases if block.strip()]

        logger.debug(f"Parsed test cases: {parsed_cases}")

        if not parsed_cases:
            return "No test cases were returned from the AI."

        save_test_cases_to_csv(parsed_cases, csv_file="my_voice_test_cases.csv")

        logger.debug(f"Success: saved test cases for story {story_id} to CSV.")
        return (
            f"Test cases for story {story_id} have been generated using the ADO data "
            "and saved to 'my_voice_test_cases.csv'."
        )

    except Exception as e:
        logger.error(f"Error in handle_test_case_generation: {e}")
        return "I encountered an error generating the test cases. Please check the logs."

if __name__ == "__main__":
    main()