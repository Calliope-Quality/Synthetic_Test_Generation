# modules/user_story_processor.py
from bs4 import BeautifulSoup

def process_user_story(user_story):
    """
    Process the user story by stripping HTML tags and returning clean text.
    """
    # Use BeautifulSoup to parse and strip HTML tags
    soup = BeautifulSoup(user_story, "html.parser")
    # Extract text, using newline as separator to maintain some formatting
    clean_text = soup.get_text(separator="\n").strip()
    return clean_text