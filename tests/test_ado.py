# test_ado.py

import os
from dotenv import load_dotenv
from logger import logger
from modules.ado_integration import get_user_story_from_ado

# Load environment variables from the .env file.
# This ensures that sensitive information such as API keys and configuration
# details (like ADO_PAT, ADO_ORG_URL, etc.) are loaded and available
# for use in our application. This step is crucial for authenticating
# and interacting with the Azure DevOps API.
load_dotenv()

def main():
    # Start the test and log the initiation process.
    logger.info("Starting ADO integration test...")

    # Call the function that fetches the user story from Azure DevOps.
    # This function encapsulates the logic for connecting to ADO,
    # authenticating with the provided credentials, and retrieving
    # the specified work item data.
    user_story = get_user_story_from_ado()

    # Check if we successfully retrieved a user story.
    # If user_story is not None or empty, then the call was successful,
    # and we can display the result. Otherwise, we log an error message.
    if user_story:
        # Log a success message and print out the retrieved user story to the console.
        logger.info("Successfully retrieved user story from ADO:")
        print(user_story)
    else:
        # If the retrieval failed, log an error. This helps with debugging
        # by making it clear that something went wrong in the ADO call.
        logger.error("Failed to retrieve user story from ADO.")

# Entry point of the script.
# This ensures that main() is called only when this script is executed directly,
# and not when it's imported as a module in another script.
if __name__ == "__main__":
    main()