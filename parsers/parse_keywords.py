from typing import List, Optional

from selenium.webdriver.common.by import By


def get_keywords(driver) -> List[Optional[str]]:
    """
    Retrieve keywords from a webpage using Selenium.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        List[Optional[str]]: List of keyword strings with optional None values.
    """
    keywords = []
    keywords_div = driver.find_element(By.CLASS_NAME, "header_genres__VbXDF")
    keyword_elements = keywords_div.find_elements(By.TAG_NAME, "span")
    for keyword in keyword_elements:
        keywords.append(keyword.text)
    return keywords
