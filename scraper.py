from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scroll import scroll_page_callback
from parser import parse_item
from database import get_db
from item_service import ItemService
from schemas import ActorOutput, ActorBaseInput, ItemDetailInput
from actor_service import ActorService


def scrape_data(
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


def scrape_details(
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

        rating_div = driver.find_element(By.CLASS_NAME, "movie_rating_front_stars__6kr8Q").get_attribute("style")
        rating_val = rating_div.split(":")[1].strip().replace("%", "").replace(";", "")

        description = driver.find_element(By.CLASS_NAME, "header_overview__vuZwx").text

        keywords = []
        keywords_div = driver.find_element(By.CLASS_NAME, "header_genres__VbXDF")
        keyword_elements = keywords_div.find_elements(By.TAG_NAME, "span")
        for keyword in keyword_elements:
            keywords.append(keyword.text)

        casts = driver.find_elements(By.CLASS_NAME, "cast")

        actors = []
        for actor in casts:
            full_name = actor.find_element(By.CLASS_NAME, "actor-name").text
            image = actor.find_element(By.CLASS_NAME, "card-img").get_attribute("src")
            url = actor.get_attribute("href")

            actor = ActorBaseInput(full_name=full_name, image=image, url=url)

            actor_obj = ActorService(next(get_db())).create_actor(actor)
            actors.append(actor_obj)

        item = ItemDetailInput(
            rating=float(rating_val),
            description=description,
            actors=actors,
            keywords=",".join(keywords)
        )
        print(item)

    except Exception as e:
        print(e)
