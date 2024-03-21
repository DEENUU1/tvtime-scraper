from sqlalchemy.orm import Session

from actor_repository import ActorRepository
from schemas import ActorOutput, ActorBaseInput


class ActorService:
    def __init__(self, session: Session):
        self.repository = ActorRepository(session)

    def create_actor(self, actor: ActorBaseInput) -> ActorOutput:
        if self.repository.actor_exists_by_full_name(actor.full_name):
            return self.repository.get_actor_by_full_name(actor.full_name)

        return self.repository.create_actor(actor)

