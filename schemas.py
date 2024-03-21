from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    title: str
    genre: str
    production_year: Optional[int] = None
    image: Optional[str] = None
    hours: Optional[int] = None
    minutes: Optional[int] = None
    url: str
    type: str
