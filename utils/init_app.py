import os

from config.database import engine
from models.actor import Actor
from models.item import Item


def init_app() -> None:
    """
    Initialize the application by creating database tables and data directory if not exists.
    """
    # Create database tables
    Item.metadata.create_all(bind=engine)
    Actor.metadata.create_all(bind=engine)

    # Create data directory if not exists
    if not os.path.exists("data"):
        os.mkdir("data")
