# modules/test_case_formatter.py

import re

def format_test_cases(ai_content: str) -> list[str]:
    # Normalize newlines
    text = ai_content.strip()

    # Modify the regex to split on lines starting with "**Test Case"
    parts = re.split(r"(\*\*Test Case\s*\d+\*\*)", text, flags=re.IGNORECASE)

    test_cases = []
    # Rebuild test case blocks using the captured delimiters
    # parts[0] may contain content before the first test case, often empty
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()  # e.g., "**Test Case 10**"
        body = parts[i+1].strip() if (i+1) < len(parts) else ""
        full_case = f"{heading}\n{body}"
        test_cases.append(full_case)

    if not test_cases:
        test_cases = [text]

    return test_cases

def parse_test_case_block(block: str) -> dict:
    """
    Parses a single test case block in the format:
    **Test Case X**
    Title: ...
    Description: ...
    Steps:
    1) ...
    2) ...
    Expected: ...
    """
    title = description = steps = expected = ""

    # Optionally remove the bold marker from the Test Case header
    # For now, we ignore the '**Test Case X**' line.

    title_match = re.search(r"Title:\s*(.*)", block, flags=re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()

    description_match = re.search(r"Description:\s*(.*)", block, flags=re.IGNORECASE)
    if description_match:
        description = description_match.group(1).strip()

    steps_match = re.search(r"Steps:\s*((?:(?!Expected:).)*)", block, flags=re.IGNORECASE | re.DOTALL)
    if steps_match:
        steps = steps_match.group(1).strip()

    expected_match = re.search(r"Expected:\s*(.*)", block, flags=re.IGNORECASE)
    if expected_match:
        expected = expected_match.group(1).strip()

    return {
        "title": title,
        "description": description,
        "steps": steps,
        "expected_outcome": expected
    }