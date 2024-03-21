from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from scroll import scroll_page_callback
from pydantic import BaseModel
from typing import Optional


BASE_URL: str = "https://www.tvtime.com/pl/genres/action?view=movies"


class Item(BaseModel):
    title: str
    genre: str
    duration: Optional[str] = None
    production_year: Optional[int] = None
    image: str
    url: str

def parse_item(item) -> Item:
    title = item.find_element(By.CLASS_NAME, "genres_genres_title___e19Y").text
    url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
    ul = item.find_element(By.CLASS_NAME, "genres_genres_submeta__W1AVW")
    li = ul.find_elements(By.TAG_NAME, "li")

    duration, production_year = None, None
    if len(li) == 3:
        duration = li[0].text
        production_year = int(li[2].text)
    genre_div = item.find_element(By.CLASS_NAME, "genres_genres_type__ic9U5")
    genre = genre_div.find_element(By.TAG_NAME, "span").text
    image = item.find_element(By.TAG_NAME, "img").get_attribute("src")

    item = Item(
        title=title,
        url=url,
        genre=genre,
        duration=duration,
        production_year=production_year,
        image=image
    )
    return item


def scrape_data(url: str) -> None:
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
            parsed_item = parse_item(item)
            print(parsed_item)
            print("\n")

    scroll_page_callback(driver, scraper)

    driver.quit()


if __name__ == "__main__":
    scrape_data(BASE_URL)
