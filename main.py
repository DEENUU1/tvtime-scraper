from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
from scroll import scroll_page_callback


BASE_URL: str = "https://www.tvtime.com/pl/genres/action?view=movies"


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
            title = item.find_element(By.CLASS_NAME, "genres_genres_title___e19Y").text
            print(title)

    scroll_page_callback(driver, scraper)

    driver.quit()


if __name__ == "__main__":
    scrape_data(BASE_URL)
