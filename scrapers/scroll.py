from time import sleep


def scroll_page_callback(driver, callback) -> None:
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        consecutive_scrolls = 0

        while consecutive_scrolls < 3:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                consecutive_scrolls += 1
            else:
                consecutive_scrolls = 0

            last_height = new_height

            callback(driver)

    except Exception as e:
        print(e)
