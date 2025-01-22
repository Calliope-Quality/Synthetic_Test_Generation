
# This can probably be deprecated with the overall config.py in a future version

import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

# API Keys and configuration
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