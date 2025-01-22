
RAG-Powered Test Case Generation

Overview

RAG-Powered Test Case Generation is a sophisticated tool designed to streamline the creation of realistic and effective test cases from user stories. By leveraging Retrieval-Augmented Generation (RAG), this project enhances user stories with historical test case data from TestRail, ensuring that the generated test cases are both relevant and comprehensive. Additionally, the integration with ElevenLabs facilitates a natural, voice-activated interaction, making the process more intuitive and efficient.

Why RAG Matters

Retrieval-Augmented Generation (RAG) is at the core of this project, playing a crucial role in transforming raw user stories into actionable test cases. Here’s why RAG is indispensable:
	•	Contextual Enrichment: RAG integrates current user stories with historical test case data, providing a richer context for AI-driven test case generation.
	•	Relevance and Precision: By accessing a repository of past test cases, RAG ensures that the generated tests align with established testing patterns and real-world scenarios.
	•	Efficiency: Automating test case generation accelerates the testing process, allowing QA teams to focus on refining and expanding the initial outputs rather than creating them from scratch.

Project Highlights

RAG-Powered Test Case Generation stands out due to its thoughtful architecture and robust functionality:
	•	Seamless Azure DevOps Integration: Directly fetches user stories from Azure DevOps (ADO), ensuring that the test cases are grounded in the latest project requirements.
	•	Flexible Database Options: Offers two powerful pathways for managing the RAG database:
	•	FAISS: Ideal for smaller datasets, FAISS provides efficient vector similarity search capabilities.
	•	ChromaDB: Suited for larger volumes of data, ChromaDB ensures scalability and performance.
	•	Voice Activation with ElevenLabs: Utilizes ElevenLabs for voice activation, enabling a more natural and hands-free interaction with the system.
	•	AI-Driven Test Case Synthesis: Employs OpenAI’s advanced models to generate up to 10 concise and relevant test cases per user story, covering both positive and negative scenarios.
	•	Comprehensive Logging and Reporting: Maintains detailed logs of all operations, facilitating easy troubleshooting and audit trails.

RAG Database Paths: FAISS vs. ChromaDB

Understanding the database options is essential for optimizing the performance of your test case generation workflow:

FAISS (Facebook AI Similarity Search)
	•	Best For: Small to medium-sized datasets.
	•	Advantages:
	•	High-speed vector similarity searches.
	•	Easy to set up and integrate.
	•	Considerations:
	•	May not scale as efficiently with extremely large datasets compared to ChromaDB.

ChromaDB
	•	Best For: Large-scale datasets requiring robust scalability.
	•	Advantages:
	•	Designed for handling vast amounts of data with ease.
	•	Offers enhanced performance for large-scale vector searches.
	•	Considerations:
	•	Slightly more complex setup compared to FAISS.

Note: Users can choose either FAISS or ChromaDB based on their dataset size and performance requirements. Ensure that the appropriate code path is selected to match the chosen database.

Data Import Paths: JSON vs. CSV

The project provides flexible methods for importing historical test case data from TestRail:

JSON Import (json_to_vector.py)
	•	Purpose: Extracts test case data from a JSON export from TestRail and inserts it into the ChromaDB vector database.
	•	Usage:

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

Ensure you replace the placeholders with your actual credentials.

3. Import Historical Test Cases

Choose your preferred database and run the appropriate import script:

Using JSON with ChromaDB
	1.	Export Test Cases from TestRail:
	•	Export your test cases from TestRail in JSON format and save them as cases.json in the project directory.
	2.	Run JSON to Vector Import:

python json_to_vector.py

This script will:
	•	Parse the cases.json file.
	•	Generate embeddings using OpenAI’s embedding models.
	•	Insert the embeddings and associated metadata into the ChromaDB collection named testrail_test_cases.

Using CSV Import (Optional)
	1.	Prepare CSV File:
	•	Ensure your CSV file contains the necessary fields such as title, description, steps, expected_outcome, etc.
	2.	Modify json_to_vector.py for CSV:
	•	Update the data extraction section in json_to_vector.py to read from your CSV file instead of JSON.
	3.	Run Modified Import Script:

python json_to_vector.py

This will parse the CSV file, generate embeddings, and insert them into the chosen vector database.

4. Run the Main Script

Initiate the voice-activated test case generation process:

python voice_chat_ado_integration_chromadb.py

Voice Chat Mode:
	•	Start Interaction: Press Enter to speak or type ‘exit’ to quit.
	•	Voice Commands: Use natural speech to request test case generation, e.g., “Generate synthetic test cases for me for User Story 1-44-329.”

5. Review Logs and Output
	•	Terminal Output: The system will print raw, formatted, and parsed test case data for verification.
	•	CSV File: Generated test cases are saved to my_voice_test_cases.csv for easy access and further analysis.
	•	Logs: Detailed logs are maintained for troubleshooting and audit purposes.

Example Workflow
	1.	Start the Script:

python voice_chat_ado_integration_chromadb.py


	2.	Interact via Voice:
	•	Prompt: “Generate synthetic test cases for me for User Story 1-44-329.”
	•	Response: The system processes the request, fetches the user story from ADO, retrieves relevant past test cases from ChromaDB, and generates new test cases using OpenAI.
	3.	Verify Output:
	•	Terminal: Displays the raw GPT-generated test cases, formatted blocks, and parsed data.
	•	CSV: Check my_voice_test_cases.csv to see the saved test cases with fields like Test Case Number, Title, Description, Steps, and Expected Outcome.

Conclusion

RAG-Powered Test Case Generation is a comprehensive tool that harnesses the capabilities of Retrieval-Augmented Generation to produce high-quality test cases from user stories. By integrating seamlessly with Azure DevOps, offering flexible database options (FAISS and ChromaDB), and incorporating voice activation through ElevenLabs, it provides a scalable and efficient solution for modern QA teams.

MIT License 

Created by Adam Satterfield