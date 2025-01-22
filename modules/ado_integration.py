# modules/ado_integration.py
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from logger import logger

load_dotenv()

# Retrieve ADO configuration from environment variables, including username
ADO_USERNAME = os.getenv('ADO_USERNAME')
ADO_PAT = os.getenv('ADO_PAT')


def get_user_story_from_ado(story_id):
    """
    Fetch the title, description, and acceptance criteria of a work item
    (user story) from Azure DevOps and concatenate them into a single string.

    Args:
        story_id (str): The work item (user story) ID to fetch.

    Returns:
        str: Concatenated title, description, and acceptance criteria,
             or an error message if not found.
    """

    # Build the work item URL dynamically using the story_id
    WORK_ITEM_URL = (
        f"URL" #your ADO URL
        f"_apis/wit/workItems/{story_id}?$expand=All&api-version=7.1-preview.3"
    )

    # Check for necessary configuration
    if not all([ADO_USERNAME, ADO_PAT]):
        logger.error("Missing ADO configuration. Please check environment variables for username and PAT.")
        return None

    auth = HTTPBasicAuth(ADO_USERNAME, ADO_PAT)

    try:
        response = requests.get(WORK_ITEM_URL, auth=auth)
        response.raise_for_status()
        work_item = response.json()

        # Extract title, description, and acceptance criteria fields safely
        fields = work_item.get('fields', {})
        title = fields.get('System.Title', '')
        description = fields.get('System.Description', '')
        acceptance_criteria = fields.get('Microsoft.VSTS.Common.AcceptanceCriteria', '')

        # Check if all key components are missing
        if not title and not description and not acceptance_criteria:
            logger.warning("The fetched work item has no title, description, or acceptance criteria.")
            return "Vague user story: missing title, description, and acceptance criteria."

        # Concatenate available parts of the user story
        user_story_parts = [part for part in (title, description, acceptance_criteria) if part]
        user_story = "\n".join(user_story_parts)
        return user_story.strip()
    except Exception as e:
        logger.error(f"Error fetching work item {story_id}: {e}")
        return None