import uuid

from sqlalchemy import Column, UUID, String, Integer, Float, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

actor_item_association = Table(
    'actor_item_association', Base.metadata,
    Column('actor_id', ForeignKey('actors.id'), primary_key=True),
    Column('item_id', ForeignKey('items.id'), primary_key=True)
)


class Actor(Base):
    __tablename__ = "actors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    items = relationship("Item", secondary=actor_item_association, back_populates="actors")


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
    details = Column(Boolean, default=False)
    rating = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    actors = relationship("Actor", secondary=actor_item_association, back_populates="items")
