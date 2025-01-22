import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import numpy as np

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

from config import DEBUG

import chromadb
import chromadb.utils.embedding_functions as embedding_functions

# ---------------------------
# 1) CREATE A PERSISTENT CLIENT (NEW API)
# ---------------------------
client = chromadb.PersistentClient(path="./chroma_db")

# ---------------------------
# 2) DEFINE CUSTOM EMBEDDING FUNCTION
# ---------------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
try:
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_api_key,
        model_name="text-embedding-3-small"
    )
except AttributeError as e:
    print("Warning: Could not find OpenAIEmbeddingFunction. Check your ChromaDB version.")
    raise e

# ---------------------------
# 3) GET OR CREATE YOUR COLLECTION
# ---------------------------
collection = client.get_or_create_collection(
    name="testrail_test_cases",
    embedding_function=openai_ef,
    metadata={"description": "TestRail test cases stored with Chroma"}
)

async def process_and_insert(executor, test_case):
    loop = asyncio.get_event_loop()

    # ---------------------------
    # BUILD TEXT FROM JSON FIELDS
    # ---------------------------
    combined_text = (
        f"Title: {test_case.get('title', '')}\n"
        f"Description: {test_case.get('custom_testcase_description', '')}\n"
        f"Preconditions: {test_case.get('custom_preconds', '')}\n"
    )

    steps = test_case.get('custom_steps_separated') or []
    if DEBUG:
        print(f"Processing test case ID {test_case.get('id')} with {len(steps)} steps.")

    for idx, step in enumerate(steps):
        step_info = (
            f"Step {idx + 1} Content: {step.get('content', '')}\n"
            f"Expected: {step.get('expected', '')}\n"
            f"Additional Info: {step.get('additional_info', '')}\n"
            f"Refs: {step.get('refs', '')}\n"
        )
        combined_text += step_info

    if DEBUG:
        print(f"Combined text for test case {test_case.get('id')} prepared. Original length: {len(combined_text)}")

    # ---------------------------
    # TRIM IF TEXT IS TOO LARGE
    # ---------------------------
    max_length = 2000
    if len(combined_text) > max_length:
        combined_text = combined_text[:max_length]
        if DEBUG:
            print(f"Trimmed text to {max_length} characters.")

    # ---------------------------
    # GENERATE EMBEDDING WITH THROTTLING
    # ---------------------------
    try:
        result = await loop.run_in_executor(executor, openai_ef, combined_text)

        if isinstance(result, list) and len(result) > 0:
            # Flatten embedding if needed
            if isinstance(result[0], np.ndarray):
                embedding = result[0].tolist()
            elif (
                isinstance(result[0], list) and
                len(result[0]) > 0 and
                isinstance(result[0][0], np.ndarray)
            ):
                embedding = [np.array(x).tolist() for x in result]
            else:
                embedding = result
        else:
            embedding = result

        # Throttle to avoid exceeding rate limits
        await asyncio.sleep(0.2)  # 0.2 seconds pause between requests

    except Exception as e:
        print(f"Error generating embedding for test case ID {test_case.get('id')}: {e}")
        return

    doc_id = str(test_case["id"])
    metadata = {
        "title": test_case.get("title"),
        "priority_id": test_case.get("priority_id"),
        "section_id": test_case.get("section_id"),
    }

    if DEBUG:
        print(f"Inserting test case ID {doc_id} into Chroma collection.")

    try:
        collection.add(
            ids=[doc_id],
            documents=[combined_text],
            embeddings=[embedding],
            metadatas=[metadata]
        )
    except Exception as e:
        print(f"Error inserting test case ID {doc_id} into collection: {e}")
        return

    if DEBUG:
        print(f"Test case ID {doc_id} inserted successfully.")

async def main():
    json_path = Path(__file__).parent / "cases.json"
    if DEBUG:
        print(f"Loading JSON data from {json_path}")

    with open(json_path, 'r') as f:
        data = json.load(f)

    if DEBUG:
        print(f"Loaded {len(data)} test cases from JSON.")

    all_data = data  # Use all test cases
    batch_size = 100  # Adjust as needed

    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(0, len(all_data), batch_size):
            batch = all_data[i:i + batch_size]
            if DEBUG:
                print(f"Processing batch {i // batch_size + 1}: Test cases {i} to {i + len(batch) - 1}")
            tasks = [process_and_insert(executor, test_case) for test_case in batch]
            await asyncio.gather(*tasks)
            if DEBUG:
                print(f"Completed batch {i // batch_size + 1}")

    if DEBUG:
        print("All test cases have been processed and inserted into Chroma.")

if __name__ == "__main__":
    asyncio.run(main())