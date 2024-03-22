from typing import List, Type, Any, Dict

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.item import Item
from repositories.item_repository import ItemRepository
from schemas.schemas import ItemBaseInput, ItemOutput, ItemDetailInput
from utils.save_to_json import save_to_json


class ItemService:
    """
    Service class for item-related operations.
    """

    def __init__(self, session: Session):
        """
        Initialize ItemService with a database session.

        Args:
            session (sqlalchemy.orm.Session): Database session.
        """
        self.item_repository = ItemRepository(session)

    def create(
            self,
            data: ItemBaseInput
    ) -> ItemBaseInput:
        """
        Create a new item if it doesn't already exist in the database.

        Args:
            data (ItemBaseInput): Item information to create.

        Returns:
            ItemBaseInput: Created item information.
        """
        if self.item_repository.item_exists_by_url(data.url):
            print("Item already exists")
        return self.item_repository.create(data)

    def update_details(
            self,
            item_url: str,
            details_data: ItemDetailInput,
            actors: List[UUID4]
    ) -> Dict[str, Any]:
        """
        Update details of an existing item.

        Args:
            item_url (str): URL of the item to update.
            details_data (ItemDetailInput): Details data to update.
            actors (List[UUID4]): List of actor IDs to associate with the item.

        Returns:
            Dict[str, Any]: Updated item information.
        """
        if not self.item_repository.item_exists_by_url(item_url):
            raise ValueError("Item does not exist")
        item = self.item_repository.get_object_by_url(item_url)
        return self.item_repository.update_details(item, details_data, actors)

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50
    ) -> List[ItemOutput]:
        """
        Retrieve all items from the database.

        Args:
            page (int): Page number.
            page_limit (int): Number of items per page.

        Returns:
            List[ItemOutput]: List of item information.
        """
        return self.item_repository.get_all(page, page_limit)

    def get_all_details_not_found(self) -> List[Type[Item]]:
        """
        Retrieve all items with missing details.

        Returns:
            List[Type[Item]]: List of items with missing details.
        """
        return self.item_repository.get_all_details_not_found()

    def export_to_json(self, page: int = 1, page_limit: int = 50) -> None:
        """
        Export items to JSON files.

        Args:
            page (int): Page number.
            page_limit (int): Number of items per page.

        Returns:
            None
        """
        page_num = page
        next_page = True

        while next_page:
            items = self.item_repository.get_all(page_num, page_limit)

            print(f"Page {page_num}")

            if len(items) < page_limit:
                next_page = False

            save_to_json(items, page_num)

            page_num += 1
