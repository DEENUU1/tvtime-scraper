from typing import Optional, List

from pydantic import BaseModel


class ItemBaseInput(BaseModel):
    title: str
    genre: str
    production_year: Optional[int] = None
    image: Optional[str] = None
    hours: Optional[int] = None
    minutes: Optional[int] = None
    url: str
    type: str


class ActorBaseInput(BaseModel):
    full_name: str


class ItemInput(ItemBaseInput):
    details: bool = False
    rating: Optional[float] = None
    description: Optional[str] = None
    actors: List[ActorBaseInput]
