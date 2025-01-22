# utils/csv_to_vector.py
import csv
from dotenv import load_dotenv
from logger import logger
from utils.vector_db_faiss import add_embedding
from utils.embeddings import generate_embedding

load_dotenv()

def import_csv_to_faiss(csv_file_path, text_columns=None):
    """
    Read test cases from a CSV file, concatenate data from specified columns,
    generate embeddings, and store them in FAISS.

    Args:
        csv_file_path (str): Path to the CSV file.
        text_columns (list): List of column names whose values should be concatenated.
                             If None, defaults to ['test_case'].
    """
    if text_columns is None:
        text_columns = ['test_case']

    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Concatenate specified columns, filtering out None values or blanks
                combined_text = " ".join(
                    (row.get(col, '') or '') for col in text_columns
                ).strip()

                if combined_text:
                    embedding = generate_embedding(combined_text)
                    add_embedding(embedding, combined_text)
                    logger.debug(f"Processed and added test case snippet: {combined_text[:50]}...")
    except Exception as e:
        logger.error(f"Error importing CSV: {e}")
