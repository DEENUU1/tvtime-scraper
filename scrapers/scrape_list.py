from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .scroll import scroll_page_callback
from parsers.parse_item import parse_item
from config.database import get_db
from services.item_service import ItemService


def scrape_list(
        _type: str,
        url: str
) -> None:
    _service = ItemService(next(get_db()))

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-consent"))
        )
        consent_button.click()
    except Exception as e:
        print(e)

    def scraper(driver) -> None:
        items = driver.find_elements(By.CLASS_NAME, "genres_genres_item__T2zjA")
        for item in items:
            parsed_item = parse_item(item, _type)
            _service.create(parsed_item)

    scroll_page_callback(driver, scraper)

    driver.quit()



