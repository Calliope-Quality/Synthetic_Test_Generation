# main.py
import os
from dotenv import load_dotenv
from logger import logger
from modules.user_story_processor import process_user_story
from modules.rag_engine_faiss import generate_test_cases
from modules.test_case_formatter import format_test_cases
from modules.ado_integration import get_user_story_from_ado
from utils.vector_db import initialize_faiss_index
from modules.test_case_exporter import parse_test_cases, save_test_cases_to_csv

# Load environment variables
load_dotenv()

def main():
    # Initialize FAISS index with the appropriate embedding dimension
    # (e.g., 1536 if using a model that outputs 1536-dim embeddings)
    initialize_faiss_index(dimension=1536)

    # Prompt user for the work item ID
    story_id = input("User story ID: ").strip()
    if not story_id:
        logger.error("No user story ID provided. Exiting.")
        return

    # Fetch user story from Azure DevOps using the entered ID
    user_story = get_user_story_from_ado(story_id)
    if not user_story:
        logger.error(f"Failed to retrieve user story with ID {story_id}.")
        return

    logger.debug(f"Fetched user story from ADO: {user_story}")

    # Process the user story
    processed_story = process_user_story(user_story)
    logger.debug(f"Processed story: {processed_story}")

    # Generate test cases using the Retrieval-Augmented Generation (RAG) approach
    raw_test_cases = generate_test_cases(processed_story)
    logger.debug(f"Raw test cases: {raw_test_cases}")

    # Format the test cases
    test_cases = format_test_cases(raw_test_cases)
    logger.info(f"Generated Test Cases:\n{test_cases}")

    # Save to CSV
    parsed = parse_test_cases(test_cases)
    save_test_cases_to_csv(parsed, csv_file="my_test_cases.csv")
if __name__ == "__main__":
    main()