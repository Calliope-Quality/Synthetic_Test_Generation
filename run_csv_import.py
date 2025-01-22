# run_csv_import.py
from dotenv import load_dotenv
from logger import logger
from utils.vector_db import initialize_faiss_index, save_faiss_index, save_metadata
from utils.csv_to_vector import import_csv_to_faiss

# Load environment variables from .env file
load_dotenv()

# Initialize the FAISS index with the appropriate embedding dimension
# Ensure this dimension matches your embedding model (e.g., 1536 for OpenAI's ada model)
initialize_faiss_index(dimension=1536)

# Update the CSV file path to your specific file located in the main directory
csv_file_path = "put your filepath here.csv"

# Define which columns to concatenate from the CSV for embedding
columns_to_concatenate = [
    'Title',
    'Plan',
    'Run',
    'Steps',
    'Steps (Expected Result)',
    'Steps (Step)'
]

# Import test cases from CSV into FAISS using the specified columns
import_csv_to_faiss(csv_file_path, text_columns=columns_to_concatenate)

# Save FAISS index and metadata to keep them in sync across runs
save_faiss_index()
save_metadata()