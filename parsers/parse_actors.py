from typing import List, Optional

from selenium.webdriver.common.by import By

from schemas.schemas import ActorBaseInput, ActorOutput
from services.actor_service import ActorService


def get_actors(casts, session) -> List[Optional[ActorOutput]]:
    """
    Retrieve actors' information from a list of cast elements.

    Args:
        casts (List[WebElement]): List of web elements representing cast members.
        session: Session object for interacting with the actor service.

    Returns:
        List[Optional[ActorOutput]]: List of actor objects with optional None values.
    """
    actors = []
    for actor in casts:
        full_name = actor.find_element(By.CLASS_NAME, "actor-name").text
        image = actor.find_element(By.CLASS_NAME, "card-img").get_attribute("src")
        actor_url = actor.get_attribute("href")

        actor_data = ActorBaseInput(full_name=full_name, image=image, url=actor_url)

        actor_obj = ActorService(session).create_actor(actor_data)
        actors.append(actor_obj)
    return actors
