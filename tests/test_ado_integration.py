# test_ado_integration.py
import logging
from config import Config
from dotenv import load_dotenv
from ado_integration import get_user_story_from_ado

# Configure logging based on global debug setting
logging.basicConfig(
    level=logging.DEBUG if Config else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    story_id = "144329"  # Specify the user story ID you want to fetch
    try:
        user_story = get_user_story_from_ado(story_id)
        print("Fetched User Story:")
        print(user_story)
    except Exception as e:
        logger.error(f"Error fetching user story {story_id}: {e}")
        print(f"Failed to fetch user story {story_id}. Check logs for details.")

if __name__ == "__main__":
    main()