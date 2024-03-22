from typing import Optional

from selenium.webdriver.common.by import By


def get_rating(driver) -> Optional[float]:
    """
    Retrieve the rating value from a webpage using Selenium.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        Optional[float]: The rating value as a float, or None if not found.
    """
    rating_val, style = None, None
    try:
        rating_div = driver.find_element(By.CLASS_NAME, "movie_rating_front_stars__6kr8Q")
        if rating_div:
            style = rating_div.get_attribute("style")
        if not style:
            return None

        rating_val = style.split(":")[1].strip().replace("%", "").replace(";", "")
        if not rating_val:
            return None

    except:
        pass

    if rating_val:
        return float(rating_val)
    return None
