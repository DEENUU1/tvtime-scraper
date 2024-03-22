from selenium.webdriver.common.by import By

from parsers.parse_item import parse_item
from services.item_service import ItemService
from .click_cookies import click_cookies
from .driver import get_driver
from .scroll import scroll_page_callback


def scrape_list(
        session,
        _type: str,
        url: str,
) -> None:
    """
    Scrape a list of items from a webpage.

    Args:
        session: Session object for interacting with the item service.
        _type (str): Type of items to scrape.
        url (str): URL of the webpage to scrape.
    """
    driver = get_driver()
    driver.get(url)

    click_cookies(driver)

    def scraper(driver) -> None:
        items = driver.find_elements(By.CLASS_NAME, "genres_genres_item__T2zjA")
        for item in items:
            parsed_item = parse_item(item, _type)
            obj = ItemService(session).create(parsed_item)
            print(f"Scrape {obj.title}")
    scroll_page_callback(driver, scraper)

    driver.quit()
