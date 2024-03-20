from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time


BASE_URL: str = "https://www.tvtime.com/pl/genres/action?view=movies"


def scrape(url: str) -> None:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        driver.get(url)

        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-consent"))
            )
            consent_button.click()
        except Exception as e:
            print(e)

        items = driver.find_elements(By.CLASS_NAME, "genres_genres_item__T2zjA")
        for item in items:
            print(item.text)

    except Exception as e:
        print(e)

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape(BASE_URL)
