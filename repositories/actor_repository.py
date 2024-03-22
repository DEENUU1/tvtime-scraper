from typing import List

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.actor import Actor
from schemas.schemas import ActorBaseInput, ActorOutput


class ActorRepository:
    """
    Repository class for database operations related to actors.
    """

    def __init__(self, session: Session):
        """
        Initialize ActorRepository with a database session.

        Args:
            session (sqlalchemy.orm.Session): Database session.
        """
        self.session = session

    def create_actor(self, actor: ActorBaseInput) -> ActorOutput:
        """
        Create a new actor in the database.

        Args:
            actor (ActorBaseInput): Actor information to create.

        Returns:
            ActorOutput: Created actor information.
        """
        actor = Actor(**actor.model_dump(exclude_none=True))
        self.session.add(actor)
        self.session.commit()
        self.session.refresh(actor)
        return ActorOutput(**actor.__dict__)

    def get_actor_by_id(self, actor_id: UUID4) -> ActorOutput:
        """
        Retrieve an actor from the database by its ID.

        Args:
            actor_id (UUID4): ID of the actor.

        Returns:
            ActorOutput: Actor information.
        """
        actor = self.session.query(Actor).filter(Actor.id == actor_id).first()
        return ActorOutput(**actor.__dict__)

    def get_object_by_id(self, actor_id: UUID4) -> Actor:
        """
        Retrieve an actor object from the database by its ID.

        Args:
            actor_id (UUID4): ID of the actor.

        Returns:
            Actor: Actor object.
        """
        return self.session.query(Actor).filter(Actor.id == actor_id).first()

    def get_all_actors(self) -> List[ActorOutput]:
        """
        Retrieve all actors from the database.

        Returns:
            List[ActorOutput]: List of actor information.
        """
        actors = self.session.query(Actor).all()
        return [ActorOutput(**actor.__dict__) for actor in actors]

    def get_actor_by_full_name(self, full_name: str) -> Actor:
        """
        Retrieve an actor from the database by full name.

        Args:
            full_name (str): Full name of the actor.

        Returns:
            Actor: Actor information.
        """
        actor = self.session.query(Actor).filter(Actor.full_name == full_name).first()
        return actor

    def actor_exists_by_full_name(self, full_name: str) -> bool:
        """
        Check if an actor exists in the database by full name.

        Args:
            full_name (str): Full name of the actor.

        Returns:
            bool: True if actor exists, False otherwise.
        """
        return self.session.query(Actor).filter(Actor.full_name == full_name).first() is not None
