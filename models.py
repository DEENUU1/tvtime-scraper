import uuid

from sqlalchemy import Column, UUID, String, Integer

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    production_year = Column(String, nullable=True)
    image = Column(String, nullable=True)
    hours = Column(Integer, nullable=True)
    minutes = Column(Integer, nullable=True)
    url = Column(String, nullable=False)
    type = Column(String, nullable=False)
