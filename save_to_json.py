import json
from schemas import Item
from typing import List


def save_to_json(items: List[Item], page: int) -> None:
    with open(f"data/items_{page}.json", "w") as f:
        json.dump([item.dict() for item in items], f, indent=4)

