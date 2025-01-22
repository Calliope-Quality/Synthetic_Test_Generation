# logger.py
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine debug mode from environment variable
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

# Configure logging level based on debug mode
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a logger instance for this module
logger = logging.getLogger(__name__)