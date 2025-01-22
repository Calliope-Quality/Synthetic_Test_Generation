# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file at the start
load_dotenv()

#OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
SELECTED_MODEL = os.getenv("SELECTED_MODEL", "openai")

# ElevenLabs Specific Configuration
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID")
ELEVENLABS_OUTPUT_FORMAT = os.getenv("ELEVENLABS_OUTPUT_FORMAT")

# Global Debug Flag

# Convert string 'true'/'false' to boolean; default to False if not set.
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "t")
class Config:
    # General configuration variables
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    # DB_PATH = os.getenv('DB_PATH', 'rag_data.db') # Deprecated

    # Add more configuration variables as needed for your project