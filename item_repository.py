from models import Item as ItemModel
from sqlalchemy.orm import Session
from schemas import ItemBaseInput, ItemDetailInput, ItemOutput, ActorOutput
from typing import List, Type
from pydantic import UUID4


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session

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
            actors: List[ActorOutput]
    ) -> ItemOutput:
        item.details = True
        item.rating = data.rating
        item.description = data.description
        item.actors = actors
        self.session.commit()
        return ItemOutput(**item.__dict__)

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

    def get_object(
            self,
            id: UUID4
    ) -> Type[ItemModel]:
        return self.session.query(ItemModel).filter(ItemModel.id == id).first()

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50
    ) -> List[ItemBaseInput]:
        items = self.session.query(ItemModel)
        offset = (page - 1) * page_limit if page > 0 else 0
        items = items.offset(offset).limit(page_limit).all()
        return [ItemSchema(**item.__dict__) for item in items]