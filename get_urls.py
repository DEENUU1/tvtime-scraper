import json
from typing import Dict


def get_urls() -> Dict[str, str]:
    with open("urls.json", "r") as f:
        urls = json.load(f)

    return urls
