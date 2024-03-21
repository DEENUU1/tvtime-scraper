from enums import TypeEnum


def check_type(url: str) -> str:
    if "?view=movies" in url:
        return TypeEnum.MOVIE.value
    else:
        return TypeEnum.SHOW.value
