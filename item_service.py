from item_repository import ItemRepository
from sqlalchemy.orm import Session
from schemas import Item
from typing import List


class ItemService:
    def __init__(self, session: Session):
        self.item_repository = ItemRepository(session)

    def create(self, data: Item) -> Item:
        if self.item_repository.item_exists_by_url(data.url):
            print("Item already exists")

        return self.item_repository.create(data)

    def get_all(self) -> List[Item]:
        return self.item_repository.get_all()
