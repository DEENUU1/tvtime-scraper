from typing import Optional, List

from pydantic import BaseModel, UUID4


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
    image: Optional[str] = None
    url: Optional[str] = None


class ActorOutput(ActorBaseInput):
    id: UUID4


class ItemDetailInput(BaseModel):
    rating: Optional[float] = None
    description: Optional[str] = None
    keywords: Optional[str] = None


class ItemOutput(BaseModel):
    id: UUID4
    title: str
    genre: str
    production_year: Optional[int] = None
    image: Optional[str] = None
    hours: Optional[int] = None
    minutes: Optional[int] = None
    url: str
    type: str
    details: Optional[bool] = False
    rating: Optional[float] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    actors: List[ActorOutput]
