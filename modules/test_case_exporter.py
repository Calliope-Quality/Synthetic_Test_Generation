# modules/test_case_exporter.py

import csv
import re
from logger import logger


def parse_test_cases(md_text):
    """
    Parse the AI-generated Markdown test cases into a structured list of dictionaries.
    This function first attempts to parse the "### Test Case X: ..." format.
    If it finds none, it falls back to the "numbered list" format such as:
        1. **Some Title**
           - **Description:** ...
           - **Expected Outcome:** ...
    Each dictionary contains 'title', 'description', 'steps', and 'expected_outcome'.
    """

    # 1) Try original "### Test Case X: ..." parser
    parsed_cases = _parse_test_cases_with_headings(md_text)

    # 2) If no cases found, try the fallback parser for bullet-numbered lists
    if not parsed_cases:
        parsed_cases = _parse_test_cases_bullet_list(md_text)

    return parsed_cases


def _parse_test_cases_with_headings(md_text):
    """
    Original parser that expects blocks starting with:
        ### Test Case [number]: ...
    and containing sections:
        **Description:**
        **Steps:**
        **Expected Outcome:**

    Changes:
    - Use re.IGNORECASE to handle '### TEST CASE 1:' or '### Test case 1:' etc.
    - Trim whitespace more defensively so we don't break on extra newlines.
    """

    # Split on lines like "### Test Case X:" ignoring case.
    # We capture the heading (group 1) so we can reconstruct each block.
    # This pattern looks for:
    #   "### Test Case" [1 or more digits], then optional colon:
    #   e.g. "### Test Case 1:", "### TEST CASE 15:", etc.
    test_case_blocks = re.split(
        r'(###\s+test\s+case\s+\d+\s*:\s*.*)',  # group 1
        md_text,
        flags=re.DOTALL | re.IGNORECASE
    )

    combined_blocks = []
    # We step in increments of 2:
    #   e.g. [0]=stuff before the 1st heading, [1]=heading, [2]=content after heading, [3]=heading2, ...
    for i in range(1, len(test_case_blocks), 2):
        heading_line = test_case_blocks[i].strip()
        content_block = test_case_blocks[i + 1].strip() if (i + 1) < len(test_case_blocks) else ""
        combined_blocks.append(heading_line + "\n" + content_block)

    parsed_cases = []
    for block in combined_blocks:
        lines = block.splitlines()
        if not lines:
            continue

        # Example heading: "### Test Case 1: My Title"
        # We remove "### " but also do a fallback if GPT used uppercase.
        # Then we parse out the "Test Case 1: My Title" portion.
        heading_line = lines[0].replace("###", "").strip()
        # At this point, heading_line might look like: "Test Case 1: My Title"

        # Use a regex to separate the "Test Case X:" part from the actual title
        # e.g. "Test Case 1: My Title" => ("Test Case 1:", "My Title")
        heading_match = re.match(r'(test\s+case\s+\d+\s*:\s*)(.*)', heading_line, flags=re.IGNORECASE)
        if heading_match:
            # e.g. heading_match.group(2) is "My Title"
            heading_line = heading_match.group(2).strip()
        else:
            # Fallback: keep entire line if not matched
            heading_line = heading_line

        # Now parse the body for Description, Steps, and Expected Outcome
        description_match = re.search(
            r'\*\*Description:\*\*\s*(.+?)(?=\n\*\*Steps:\*\*|\n\*\*Expected Outcome:\*\*|\Z)', block,
            flags=re.DOTALL | re.IGNORECASE)
        steps_match = re.search(r'\*\*Steps:\*\*\s*(.+?)(?=\n\*\*Expected Outcome:\*\*|\Z)', block,
                                flags=re.DOTALL | re.IGNORECASE)
        expected_match = re.search(r'\*\*Expected Outcome:\*\*\s*(.+)', block, flags=re.DOTALL | re.IGNORECASE)

        description = (description_match.group(1).strip() if description_match else "")
        steps = (steps_match.group(1).strip() if steps_match else "")
        expected_outcome = (expected_match.group(1).strip() if expected_match else "")

        parsed_cases.append({
            "title": heading_line,
            "description": description,
            "steps": steps,
            "expected_outcome": expected_outcome
        })

    return parsed_cases


def _parse_test_cases_bullet_list(md_text):
    """
    Fallback parser that looks for lines like:
        1. **Some Title**
          - **Description:** ...
          - **Expected Outcome:** ...
        2. **Another Title**
    plus an optional "**Steps:** ..." segment.
    """
    # Split on pattern: <number>.<whitespace>**Some Title**
    # This captures lines like: "1. **Successful Registration Logging Test**"
    bullet_blocks = re.split(r'(\d+\.\s+\*\*.+?\*\*)', md_text)
    combined_blocks = []
    for i in range(1, len(bullet_blocks), 2):
        title_line = bullet_blocks[i].strip()
        content_block = bullet_blocks[i + 1].strip() if (i + 1) < len(bullet_blocks) else ""
        combined_blocks.append(title_line + "\n" + content_block)

    parsed_cases = []
    for block in combined_blocks:
        # e.g. "1. **Title**\n- **Description:** ... - **Steps:** ... - **Expected Outcome:** ..."
        # Extract the numbered title
        title_match = re.search(r'\d+\.\s+\*\*(.+?)\*\*', block)
        title_text = title_match.group(1).strip() if title_match else "Untitled Test"

        desc_match = re.search(r'\*\*Description:\*\*\s*(.+?)(?=\n- \*\*|\Z)', block, flags=re.DOTALL | re.IGNORECASE)
        steps_match = re.search(r'\*\*Steps:\*\*\s*(.+?)(?=\n- \*\*|\Z)', block, flags=re.DOTALL | re.IGNORECASE)
        outcome_match = re.search(r'\*\*Expected Outcome:\*\*\s*(.+)', block, flags=re.DOTALL | re.IGNORECASE)

        description = desc_match.group(1).strip() if desc_match else ""
        steps = steps_match.group(1).strip() if steps_match else ""
        expected_outcome = outcome_match.group(1).strip() if outcome_match else ""

        parsed_cases.append({
            "title": title_text,
            "description": description,
            "steps": steps,
            "expected_outcome": expected_outcome
        })

    return parsed_cases


def save_test_cases_to_csv(parsed_test_cases, csv_file="generated_test_cases.csv"):
    """
    Write the parsed test cases to a CSV file with columns:
    [Test Case, Description, Steps, Expected Outcome].

    Args:
        parsed_test_cases (list of dict): List of dictionaries containing test case data.
        csv_file (str): Path to save the CSV file.
    """
    if not parsed_test_cases:
        logger.warning("No test cases to write to CSV.")
        return

    fieldnames = ["Test Case", "Description", "Steps", "Expected Outcome"]

    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for tc in parsed_test_cases:
                writer.writerow({
                    "Test Case": tc.get("title", "").strip(),
                    "Description": tc.get("description", "").strip(),
                    "Steps": tc.get("steps", "").strip(),
                    "Expected Outcome": tc.get("expected_outcome", "").strip()
                })

        logger.info(f"Test cases successfully written to '{csv_file}'.")
    except Exception as e:
        logger.error(f"Error writing test cases to CSV: {e}")