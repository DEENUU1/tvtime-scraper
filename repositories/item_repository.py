from typing import List, Type, Any, Dict

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.actor import Actor
from models.item import Item as ItemModel
from repositories.actor_repository import ActorRepository
from schemas.schemas import ItemBaseInput, ItemDetailInput, ItemOutput, ActorOutput


class ItemRepository:
    """
    Repository class for database operations related to items.
    """

    def __init__(self, session: Session):
        """
        Initialize ItemRepository with a database session.

        Args:
            session (sqlalchemy.orm.Session): Database session.
        """
        self.session = session
        self.actor_repository = ActorRepository(session)

    def create(
            self,
            data: ItemBaseInput
    ) -> ItemBaseInput:
        """
        Create a new item in the database.

        Args:
            data (ItemBaseInput): Data to create the item.

        Returns:
            ItemBaseInput: Created item.
        """
        item = ItemModel(**data.model_dump(exclude_none=True))
        self.session.add(item)
        self.session.commit()
        return item

    def update_details(
            self,
            item: Type[ItemModel],
            data: ItemDetailInput,
            actors: List[Type[Actor]]
    ) -> Dict[str, Any]:
        """
        Update item details in the database.

        Args:
            item (Type[ItemModel]): Item to update.
            data (ItemDetailInput): Details to update.
            actors (List[Type[Actor]]): Actors associated with the item.

        Returns:
            Dict[str, Any]: Updated item details.
        """
        item.details = True
        item.rating = data.rating
        item.description = data.description
        item.keywords = data.keywords

        for actor in actors:
            actor_obj = self.actor_repository.get_object_by_id(actor.id)
            item.actors.append(actor_obj)

        self.session.commit()

        return {
            "id": item.id,
            "title": item.title,
            "genre": item.genre,
            "production_year": item.production_year,
            "image": item.image,
            "hours": item.hours,
            "minutes": item.minutes,
            "url": item.url,
            "type": item.type,
            "rating": item.rating,
            "description": item.description,
            "keywords": item.keywords,
            "details": item.details,
            "actors": [actor.full_name for actor in item.actors],
        }

    def item_exists_by_url(
            self,
            url: str
    ) -> bool:
        """
        Check if an item exists in the database by URL.

        Args:
            url (str): URL of the item.

        Returns:
            bool: True if the item exists, False otherwise.
        """
        return self.session.query(ItemModel).filter(ItemModel.url == url).first() is not None

    def item_exists_by_id(
            self,
            id: UUID4
    ) -> bool:
        """
        Check if an item exists in the database by ID.

        Args:
            id (UUID4): ID of the item.

        Returns:
            bool: True if the item exists, False otherwise.
        """
        return self.session.query(ItemModel).filter(ItemModel.id == id).first() is not None

    def get_object_by_id(
            self,
            id: UUID4
    ) -> Type[ItemModel]:
        """
        Retrieve an item from the database by ID.

        Args:
            id (UUID4): ID of the item.

        Returns:
            Type[ItemModel]: Retrieved item.
        """
        return self.session.query(ItemModel).filter(ItemModel.id == id).first()

    def get_object_by_url(
            self,
            url: str
    ) -> Type[ItemModel]:
        """
        Retrieve an item from the database by URL.

        Args:
            url (str): URL of the item.

        Returns:
            Type[ItemModel]: Retrieved item.
        """
        return self.session.query(ItemModel).filter(ItemModel.url == url).first()

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50
    ) -> List[ItemOutput]:
        """
        Retrieve all items from the database.

        Args:
            page (int): Page number.
            page_limit (int): Limit of items per page.

        Returns:
            List[ItemOutput]: List of retrieved items.
        """
        items = self.session.query(ItemModel)
        offset = (page - 1) * page_limit if page > 0 else 0
        items = items.offset(offset).limit(page_limit).all()

        item_outputs = []
        for item in items:
            actors_output = [
                ActorOutput(
                    id=actor.id,
                    full_name=actor.full_name,
                    image=actor.image,
                    url=actor.url
                ) for actor in item.actors
            ]
            item_output = ItemOutput(
                id=item.id,
                title=item.title,
                genre=item.genre,
                production_year=item.production_year,
                image=item.image,
                hours=item.hours,
                minutes=item.minutes,
                url=item.url,
                type=item.type,
                details=item.details,
                rating=item.rating,
                description=item.description,
                keywords=item.keywords,
                actors=actors_output
            )
            item_outputs.append(item_output)
        return item_outputs

    def get_all_details_not_found(self) -> List[Type[ItemModel]]:
        """
        Retrieve all items from the database where details are not found.

        Returns:
            List[Type[ItemModel]]: List of items with details not found.
        """
        return self.session.query(ItemModel).filter(ItemModel.details == False).all()
