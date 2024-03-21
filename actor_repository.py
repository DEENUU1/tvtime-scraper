from schemas import ActorBaseInput, ActorOutput
from sqlalchemy.orm import Session
from models import Actor
from typing import List


class ActorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_actor(self, actor: ActorBaseInput) -> ActorOutput:
        actor = Actor(**actor.model_dump(exclude_none=True))
        self.session.add(actor)
        self.session.commit()
        self.session.refresh(actor)
        return ActorOutput(**actor.__dict__)

    def get_actor_by_id(self, actor_id: int) -> ActorOutput:
        actor = self.session.query(Actor).filter(Actor.id == actor_id).first()
        return ActorOutput(**actor.__dict__)

    def get_all_actors(self) -> List[ActorOutput]:
        actors = self.session.query(Actor).all()
        return [ActorOutput(**actor.__dict__) for actor in actors]

    def get_actor_by_full_name(self, full_name: str) -> ActorOutput:
        actor = self.session.query(Actor).filter(Actor.full_name == full_name).first()
        return ActorOutput(**actor.__dict__)
