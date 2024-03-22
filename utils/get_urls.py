import json
from typing import Dict


def get_urls() -> Dict[str, str]:
    """
    Load URLs from a JSON file.

    Returns:
        Dict[str, str]: Dictionary containing URLs.
    """
    with open("urls.json", "r") as f:
        urls = json.load(f)

    return urls
