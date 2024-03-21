from actor_repository import ActorRepository
from models import Item as ItemModel, Actor
from sqlalchemy.orm import Session
from schemas import ItemBaseInput, ItemDetailInput, ItemOutput
from typing import List, Type, Any, Dict
from pydantic import UUID4


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session
        self.actor_repository = ActorRepository(session)

    def create(
            self,
            data: ItemBaseInput
    ) -> ItemBaseInput:
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
        item.details = True
        item.rating = data.rating
        item.description = data.description
        item.keywords = data.keywords

        for actor in actors:
            actor_obj = self.actor_repository.get_object_by_id(actor.id)
            item.actors.append(actor_obj)

        self.session.commit()

        return {
            "id":  item.id,
            "title": item.title,
            "genre": item.genre,
            "production_year":  item.production_year,
            "image": item.image,
            "hours":  item.hours,
            "minutes": item.minutes,
            "url": item.url,
            "type": item.type,
            "rating": item.rating,
            "description": item.description,
            "keywords": item.keywords,
            "details": item.details,
            "actors": [actor.full_name for actor in item.actors],
        }
        # return ItemOutput(**item.__dict__)

    def item_exists_by_url(
            self,
            url: str
    ) -> bool:
        return self.session.query(ItemModel).filter(ItemModel.url == url).first() is not None

    def item_exists_by_id(
            self,
            id: UUID4
    ) -> bool:
        return self.session.query(ItemModel).filter(ItemModel.id == id).first() is not None

    def get_object_by_id(
            self,
            id: UUID4
    ) -> Type[ItemModel]:
        return self.session.query(ItemModel).filter(ItemModel.id == id).first()

    def get_object_by_url(
            self,
            url: str
    ) -> Type[ItemModel]:
        return self.session.query(ItemModel).filter(ItemModel.url == url).first()

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50
    ) -> List[ItemBaseInput]:
        items = self.session.query(ItemModel)
        offset = (page - 1) * page_limit if page > 0 else 0
        items = items.offset(offset).limit(page_limit).all()
        return [ItemBaseInput(**item.__dict__) for item in items]

    def get_all_details_not_found(self) -> List[Type[ItemModel]]:
        return self.session.query(ItemModel).filter(ItemModel.details == False).all()
