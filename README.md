# RAG-Powered Test Case Generation

## Overview

RAG-Powered Test Case Generation is a sophisticated tool designed to streamline the creation of realistic and effective test cases from user stories. By leveraging Retrieval-Augmented Generation (RAG), this project enhances user stories with historical test case data from TestRail, ensuring that the generated test cases are both relevant and comprehensive. Additionally, the integration with ElevenLabs facilitates a natural, voice-activated interaction, making the process more intuitive and efficient.

## Why RAG Matters

Retrieval-Augmented Generation (RAG) is at the core of this project, playing a crucial role in transforming raw user stories into actionable test cases. Here’s why RAG is indispensable:

- **Contextual Enrichment**: RAG integrates current user stories with historical test case data, providing a richer context for AI-driven test case generation.
- **Relevance and Precision**: By accessing a repository of past test cases, RAG ensures that the generated tests align with established testing patterns and real-world scenarios.
- **Efficiency**: Automating test case generation accelerates the testing process, allowing QA teams to focus on refining and expanding the initial outputs rather than creating them from scratch.

## Project Highlights

RAG-Powered Test Case Generation stands out due to its thoughtful architecture and robust functionality:

- **Seamless Azure DevOps Integration**: Directly fetches user stories from Azure DevOps (ADO), ensuring that the test cases are grounded in the latest project requirements.
- **Flexible Database Options**: Offers two powerful pathways for managing the RAG database:
  - **FAISS**: Ideal for smaller datasets, FAISS provides efficient vector similarity search capabilities.
  - **ChromaDB**: Suited for larger volumes of data, ChromaDB ensures scalability and performance.
- **Voice Activation with ElevenLabs**: Utilizes ElevenLabs for voice activation, enabling a more natural and hands-free interaction with the system.
- **AI-Driven Test Case Synthesis**: Employs OpenAI’s advanced models to generate up to 10 concise and relevant test cases per user story, covering both positive and negative scenarios.
- **Comprehensive Logging and Reporting**: Maintains detailed logs of all operations, facilitating easy troubleshooting and audit trails.

## RAG Database Paths: FAISS vs. ChromaDB

Understanding the database options is essential for optimizing the performance of your test case generation workflow:

### FAISS (Facebook AI Similarity Search)

- **Best For**: Small to medium-sized datasets.
- **Advantages**:
  - High-speed vector similarity searches.
  - Easy to set up and integrate.
- **Considerations**:
  - May not scale as efficiently with extremely large datasets compared to ChromaDB.

### ChromaDB

- **Best For**: Large-scale datasets requiring robust scalability.
- **Advantages**:
  - Designed for handling vast amounts of data with ease.
  - Offers enhanced performance for large-scale vector searches.
- **Considerations**:
  - Slightly more complex setup compared to FAISS.

**Note**: Users can choose either FAISS or ChromaDB based on their dataset size and performance requirements. Ensure that the appropriate code path is selected to match the chosen database.

## Data Import Paths: JSON vs. CSV

The project provides flexible methods for importing historical test case data from TestRail:

### JSON Import (`json_to_vector.py`)

- **Purpose**: Extracts test case data from a JSON export from TestRail and inserts it into the ChromaDB vector database.
- **Usage**:

  ```bash
  python json_to_vector.py

	•	Process:
	1.	Extract Data: Parses the cases.json file exported from TestRail.
	2.	Generate Embeddings: Uses OpenAI’s embedding models to convert text data into vector embeddings.
	3.	Insert into ChromaDB: Stores the embeddings and associated metadata in the ChromaDB collection.

CSV Import (Optional)
	•	Purpose: Allows users to import test case data from a CSV file instead of JSON.
	•	Usage: Requires modifying the json_to_vector.py script to handle CSV parsing.
	•	Process:
	1.	Modify Script: Adjust the data extraction section in json_to_vector.py to read from a CSV file.
	2.	Run Import: Execute the modified script to insert CSV data into ChromaDB or FAISS.

Note: While the primary data import method is through JSON, users comfortable with Python can customize the import process to accommodate CSV files by adjusting the data parsing logic in the json_to_vector.py script.

Voice Activation with ElevenLabs

To enhance user experience, ElevenLabs is integrated for voice activation. This allows users to interact with the system using natural speech, making the process more intuitive and efficient. Whether you’re generating test cases or navigating through the tool, voice commands simplify interactions and reduce the need for manual inputs.

Purpose and Workflow

The primary objective of this project is to generate useful and realistic test cases derived from user stories using the power of RAG. Here’s how the process unfolds:
	1.	Import Historical Data (Optional):
	•	Utilize json_to_vector.py to parse a JSON export of past test cases from TestRail and store them in the chosen FAISS or ChromaDB vector index.
	•	This step enriches the AI’s understanding by providing a foundation of existing testing patterns.
	2.	Retrieve User Story from ADO:
	•	voice_chat_ado_integration_chromadb.py calls get_user_story_from_ado() to fetch a specific work item from Azure DevOps.
	•	The retrieved user story is processed (e.g., stripping HTML) to ensure consistency and clarity.
	3.	RAG + OpenAI Prompt Construction:
	•	The processed story is converted into an embedding.
	•	search_similar() retrieves relevant test cases from the vector database.
	•	The combined information forms a comprehensive prompt sent to OpenAI, guiding the AI to generate up to 10 synthetic test cases.
	4.	Synthesize Test Cases:
	•	OpenAI returns a structured set of test cases that address key requirements, compliance, and security considerations.
	•	These test cases are printed to the terminal for verification and saved to my_voice_test_cases.csv for further use.
	5.	Extend & Customize:
	•	QA teams review the generated test cases, refining and expanding them as needed.
	•	This collaborative step ensures that the test cases fully cover all aspects of the user story and adapt to evolving requirements.

Getting Started

1. Install Dependencies

Ensure you have Python installed. Then, install the required packages:

pip install -r requirements.txt

This will install FAISS, ChromaDB, OpenAI, ElevenLabs, and other necessary libraries.

2. Configure Environment Variables

Create a .env file in the root directory and add the following variables:

ADO_USERNAME=your_ado_username
ADO_PAT=your_ado_personal_access_token
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
DEBUG=True  # Set to False in production

Apologies for the cutoff! Here’s the continuation and conclusion of the Getting Started section, along with the File Structure addition you requested.

2. Configure Environment Variables (continued)

Ensure you replace the placeholders with your actual credentials:

ADO_USERNAME=your_ado_username
ADO_PAT=your_ado_personal_access_token
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
DEBUG=True  # Set to False in production

3. Import Historical Test Cases

To build the RAG database, use json_to_vector.py for JSON files exported from TestRail:

python json_to_vector.py

This script:
	•	Parses the cases.json file.
	•	Generates embeddings using OpenAI models.
	•	Stores the data in ChromaDB for efficient retrieval.

If you want to use a CSV import instead, modify the json_to_vector.py script to handle CSV parsing.

4. Run the Main Script

Start the voice-activated test case generation process with:

python voice_chat_ado_integration_chromadb.py

Voice Commands: Use natural language to request test case generation, e.g.,
“Generate synthetic test cases for User Story 144329.”

5. Review Logs and Output
	•	Terminal: Displays the raw, formatted, and parsed test case data.
	•	CSV File: Generated test cases are saved to my_voice_test_cases.csv for easy access.
	•	Logs: Detailed logs help with troubleshooting and tracking.

File Structure

Here’s the current file structure of the project, including tests:

Synthetic_Test_Generation/
├── README.md
├── .env.example
├── requirements.txt
├── json_to_vector.py
├── voice_chat_ado_integration_chromadb.py
├── modules/
│   ├── ado_integration.py
│   ├── logger.py
│   ├── rag_engine_chroma.py
│   ├── rag_engine_faiss.py
│   ├── test_case_exporter.py
│   ├── test_case_formatter.py
│   ├── user_story_processor.py
├── utils/
│   ├── vector_db.py
│   ├── chromadb/
│   │   ├── chroma.sqlite3
│   │   └── metadata/
├── tests/
│   ├── test_rag_chroma.py
│   ├── test_json_to_vector.py
│   ├── test_voice_integration.py

Example Workflow
	1.	Export test cases from TestRail as a JSON file and save it as cases.json.
	2.	Run json_to_vector.py to populate ChromaDB.
	3.	Start voice_chat_ado_integration_chromadb.py and interact with Calliope using voice commands.
	4.	Review generated test cases in my_voice_test_cases.csv.

Next Steps
	•	LangGraph Integration: Enhance memory and state handling for better continuity in conversations.
	•	CSV Import Support: Streamline support for alternative data sources.
	•	Performance Optimization: Expand the project’s scalability for even larger datasets.

MIT License
Created by Adam Satterfield with help from o1
