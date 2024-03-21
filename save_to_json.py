import json
from typing import List

from encoder import UUIDEncoder
from schemas import ItemOutput


def save_to_json(
        items: List[ItemOutput],
        page: int
) -> None:
    with open(f"data/items_{page}.json", "w") as f:
        json.dump(
            [item.dict() for item in items],
            f,
            indent=4,
            cls=UUIDEncoder
        )
