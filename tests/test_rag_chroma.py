# test_rag_chroma.py

from modules.rag_engine_chroma import generate_test_cases_chroma

def main():
    # Sample user story
    test_story = "As a doctor, I want to check that my prescriptions can have a start date, so that my prescriptions are filled properly."

    # Call the RAG function
    print("Running RAG for sample user story...\n")
    test_cases = generate_test_cases_chroma(test_story)

    # Output the results
    print("\nGenerated Test Cases:\n")

    if test_cases and not test_cases.startswith("ERROR:"):
        print(test_cases)
    else:
        print(f"Something went wrong: {test_cases}")

if __name__ == "__main__":
    main()