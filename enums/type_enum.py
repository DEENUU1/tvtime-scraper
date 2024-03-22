from enum import Enum


class TypeEnum(Enum):
    """
    Enumeration representing types of media content.

    Attributes:
        MOVIE (str): Represents a movie.
        SHOW (str): Represents a show.
    """
    MOVIE = "Movie"
    SHOW = "Show"
