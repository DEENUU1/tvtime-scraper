from enums.type_enum import TypeEnum


def check_type(url: str) -> str:
    """
    Check the type of content based on the URL.

    Args:
        url (str): URL of the content.

    Returns:
        str: Type of content, either "Movie" or "Show".
    """
    if "?view=movies" in url:
        return TypeEnum.MOVIE.value
    else:
        return TypeEnum.SHOW.value
