from selenium.webdriver.common.by import By

from schemas.schemas import ItemBaseInput
from utils.duration_convert import convert_duration_to_time


def parse_item(
        item, _type: str
) -> ItemBaseInput:
    """
    Parse the HTML element representing an item and extract relevant information.

    Args:
        item (selenium.webdriver.remote.webelement.WebElement): The HTML element representing an item.
        _type (str): The type of the item, either "Movie" or "Show".

    Returns:
        ItemBaseInput: An object containing parsed information about the item.

    """
    title = item.find_element(By.CLASS_NAME, "genres_genres_title___e19Y").text
    url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
    ul = item.find_element(By.CLASS_NAME, "genres_genres_submeta__W1AVW")
    li = ul.find_elements(By.TAG_NAME, "li")

    duration, production_year = None, None
    if len(li) == 3:
        duration = li[0].text
        production_year = int(li[2].text)
    if len(li) == 1:
        element = li[0].text
        if "h" in element or "m" in element:
            duration = element
        if len(element) == 4:
            production_year = int(element)

    converted_duration = convert_duration_to_time(duration)
    hours, minutes = None, None
    if converted_duration:
        hours, minutes = converted_duration.get("hours"), converted_duration.get("minutes")

    genre_div = item.find_element(By.CLASS_NAME, "genres_genres_type__ic9U5")
    genre = genre_div.find_element(By.TAG_NAME, "span").text
    image = item.find_element(By.TAG_NAME, "img").get_attribute("src")

    item = ItemBaseInput(
        title=title,
        url=url,
        genre=genre,
        production_year=production_year,
        hours=hours,
        minutes=minutes,
        image=image,
        type=_type
    )
    return item
