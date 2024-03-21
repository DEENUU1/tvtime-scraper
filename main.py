import json
from typing import Optional, Dict

from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scroll import scroll_page_callback

BASE_URL: str = "https://www.tvtime.com/pl/genres/action?view=movies"


class Item(BaseModel):
    title: str
    genre: str
    production_year: Optional[int] = None
    image: Optional[str]
    hours: Optional[int] = None
    minutes: Optional[int] = None
    url: str
    type: str


def convert_duration_to_time(duration: Optional[str]) -> Optional[Dict[Optional[int], Optional[int]]]:
    # 2h 2m
    # 1h 33m
    if not duration:
        return None

    hours, minutes = None, None

    if "h" in duration and "m" in duration:
        h_index = duration.index("h")
        m_index = duration.index("m")

        hours = int(duration[:h_index])
        minutes = int(duration[h_index + 1:m_index])

    if "h" in duration and "m" not in duration:
        h_index = duration.index("h")
        hours = int(duration[:h_index])

    if "h" not in duration and "m" in duration:
        m_index = duration.index("m")
        minutes = int(duration[:m_index])

    return {"hours": hours, "minutes": minutes}


def parse_item(item, _type: str) -> Item:
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

    item = Item(
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


def scrape_data(_type: str, url: str) -> None:
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
            print(parsed_item)

    scroll_page_callback(driver, scraper)

    driver.quit()


def get_urls() -> Dict[str, str]:
    with open("urls.json", "r") as f:
        urls = json.load(f)

    return urls


def main() -> None:
    urls = get_urls()

    for k, v in urls.items():
        _type = None
        if k.endswith("s"):
            _type = "Show"
        if k.endswith("m"):
            _type = "Movie"

        scrape_data(k, v)


if __name__ == "__main__":
    main()
