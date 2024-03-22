from selenium.webdriver.common.by import By

from parsers.parse_actors import get_actors
from parsers.parse_keywords import get_keywords
from parsers.parse_rating import get_rating
from schemas.schemas import ItemDetailInput
from services.item_service import ItemService
from .click_cookies import click_cookies
from .driver import get_driver


def scrape_details(
        session,
        url: str
) -> None:
    """
    Scrape details of an item from a webpage.

    Args:
        session: Session object for interacting with the item service.
        url (str): URL of the webpage to scrape.
    """
    driver = get_driver()
    driver.get(url)

    click_cookies(driver)

    description = driver.find_element(By.CLASS_NAME, "header_overview__vuZwx").text
    rating_val = get_rating(driver)
    keywords = get_keywords(driver)

    casts = driver.find_elements(By.CLASS_NAME, "cast")
    actors = get_actors(casts, session)

    item = ItemDetailInput(
        rating=rating_val,
        description=description,
        actors=actors,
        keywords=",".join(keywords)
    )

    item = ItemService(session).update_details(url, item, actors)
    print(item)
