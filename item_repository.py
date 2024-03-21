from models import Item as ItemModel
from sqlalchemy.orm import Session
from schemas import Item as ItemSchema
from typing import List


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
            self,
            data: ItemSchema
    ) -> ItemSchema:
        item = ItemModel(**data.model_dump(exclude_none=True))
        self.session.add(item)
        self.session.commit()
        return item

    def item_exists_by_url(
            self,
            url: str
    ) -> bool:
        return self.session.query(ItemModel).filter(ItemModel.url == url).first() is not None

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50
    ) -> List[ItemSchema]:
        items = self.session.query(ItemModel)
        offset = (page - 1) * page_limit if page > 0 else 0
        items = items.offset(offset).limit(page_limit).all()
        return [ItemSchema(**item.__dict__) for item in items]