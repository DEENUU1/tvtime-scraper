import os

from database import engine
from models import Item


def init_app() -> None:
    Item.metadata.create_all(bind=engine)
    if not os.path.exists("data"):
        os.mkdir("data")
