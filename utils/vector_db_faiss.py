# utils/vector_db_faiss.py
import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from logger import logger

load_dotenv()

# Files to save/load
INDEX_FILE = "faiss_index_file.index"
METADATA_FILE = "faiss_metadata.json"

# Global references
INDEX = None
METADATA = []  # Will store metadata (e.g., original text) corresponding to each embedding vector

def initialize_faiss_index(dimension: int):
    """
    Initialize a FAISS index with the given vector dimension.
    Loads existing index and metadata if found; otherwise, creates a new index.
    """
    global INDEX, METADATA
    if os.path.exists(INDEX_FILE):
        # Load the existing FAISS index
        INDEX = faiss.read_index(INDEX_FILE)
        logger.info(f"FAISS index loaded from {INDEX_FILE}. Size: {INDEX.ntotal}")

        # Load metadata if it exists
        if os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                METADATA = json.load(f)
            logger.info(f"Loaded metadata with {len(METADATA)} entries.")
        else:
            logger.warning("No metadata file found. METADATA is empty.")
    else:
        # Create a new FAISS index if none exists
        INDEX = faiss.IndexFlatL2(dimension)
        logger.info(f"New FAISS index initialized with dimension {dimension}.")
        METADATA = []

    return INDEX


def get_faiss_index():
    """Return the current FAISS index (or None if not initialized)."""
    return INDEX


def add_embedding(embedding, metadata_item):
    """
    Add an embedding to the FAISS index, appending corresponding metadata.

    Args:
        embedding (list or np.array): The vector representation (dimension must match FAISS index).
        metadata_item (any): The metadata associated with this embedding (e.g., original text).
    """
    global INDEX, METADATA

    if INDEX is None:
        logger.error("FAISS index is not initialized. Cannot add embedding.")
        return

    # Convert embedding to a float32 Numpy array with shape (1, dimension)
    vector = np.array([embedding], dtype='float32')

    INDEX.add(vector)
    METADATA.append(metadata_item)
    logger.debug(f"Added embedding. Index size: {INDEX.ntotal}, METADATA length: {len(METADATA)}")


def search_similar(embedding, top_k=5):
    """
    Search for the top_k similar items in the FAISS index given an embedding.
    Returns a list of metadata items that match.

    Args:
        embedding (list or np.array): The query vector.
        top_k (int): Number of nearest neighbors to retrieve.

    Returns:
        list: Metadata of the top_k most similar items.
    """
    global INDEX, METADATA

    if INDEX is None or INDEX.ntotal == 0:
        logger.warning("FAISS index is not initialized or empty.")
        return []

    query_vector = np.array([embedding], dtype='float32')
    distances, indices = INDEX.search(query_vector, top_k)

    similar_items = []
    for idx in indices[0]:
        # Validate the returned index before using it
        if 0 <= idx < len(METADATA):
            similar_items.append(METADATA[idx])
        else:
            logger.warning(f"Invalid index {idx} encountered during search.")
    return similar_items


def save_faiss_index():
    """
    Persist the FAISS index to disk.
    """
    global INDEX
    if INDEX is not None:
        faiss.write_index(INDEX, INDEX_FILE)
        logger.info(f"FAISS index saved to {INDEX_FILE}.")
    else:
        logger.error("No FAISS index to save.")


def save_metadata():
    """
    Save the in-memory metadata array to a JSON file.
    """
    global METADATA
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(METADATA, f)
    logger.info(f"Metadata saved to {METADATA_FILE}.")