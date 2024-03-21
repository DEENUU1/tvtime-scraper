from pydantic import UUID4

from item_repository import ItemRepository
from sqlalchemy.orm import Session
from schemas import ItemBaseInput, ActorOutput, ItemOutput, ItemDetailInput
from typing import List
from save_to_json import save_to_json


class ItemService:
    def __init__(self, session: Session):
        self.item_repository = ItemRepository(session)

    def create(
            self,
            data: ItemBaseInput
    ) -> ItemBaseInput:
        if self.item_repository.item_exists_by_url(data.url):
            print("Item already exists")

        return self.item_repository.create(data)

    def update_details(
            self,
            item_id: UUID4,
            details_data: ItemDetailInput,
            actors: List[ActorOutput]
    ) -> ItemOutput:
        if self.item_repository.item_exists_by_id(item_id):
            raise "Item does not exists"

        item = self.item_repository.get_object(item_id)

        return self.item_repository.update_details(item, details_data, actors)

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50
    ) -> List[ItemBaseInput]:
        return self.item_repository.get_all(page, page_limit)

    def export_to_json(self, page: int = 1, page_limit: int = 50) -> None:
        page_num = page
        next_page = True

        while next_page:
            offers = self.item_repository.get_all(page_num, page_limit)

            print(f"Page {page_num}")

            if len(offers) < page_limit:
                next_page = False

            save_to_json(offers, page_num)

            page_num += 1
