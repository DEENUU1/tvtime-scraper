from sqlalchemy.orm import Session

from actor_repository import ActorRepository
from models import Actor
from schemas import ActorBaseInput


class ActorService:
    def __init__(self, session: Session):
        self.repository = ActorRepository(session)

    def create_actor(self, actor: ActorBaseInput) -> Actor:
        if self.repository.actor_exists_by_full_name(actor.full_name):
            return self.repository.get_actor_by_full_name(actor.full_name)

        return self.repository.create_actor(actor)

