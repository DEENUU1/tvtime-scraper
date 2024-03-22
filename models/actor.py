import uuid

from sqlalchemy import Column, UUID, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base


actor_item_association = Table(
    'actor_item_association', Base.metadata,
    Column('actor_id', ForeignKey('actors.id'), primary_key=True),
    Column('item_id', ForeignKey('items.id'), primary_key=True)
)


class Actor(Base):
    __tablename__ = "actors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    image = Column(String, nullable=True)
    items = relationship("Item", secondary=actor_item_association, back_populates="actors")
