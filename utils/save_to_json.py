import json
from typing import List

from schemas.schemas import ItemOutput
from .encoder import UUIDEncoder


def save_to_json(
        items: List[ItemOutput],
        page: int
) -> None:
    """
    Save items to a JSON file.

    Args:
        items (List[ItemOutput]): List of items to save.
        page (int): Page number.

    Returns:
        None
    """
    with open(f"data/items_{page}.json", "w") as f:
        json.dump(
            [item.dict() for item in items],
            f,
            indent=4,
            cls=UUIDEncoder
        )
