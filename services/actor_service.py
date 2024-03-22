from sqlalchemy.orm import Session

from repositories.actor_repository import ActorRepository
from schemas.schemas import ActorBaseInput, ActorOutput


class ActorService:
    """
    Service class for actor-related operations.
    """

    def __init__(self, session: Session):
        """
        Initialize ActorService with a database session.

        Args:
            session (sqlalchemy.orm.Session): Database session.
        """
        self.repository = ActorRepository(session)

    def create_actor(self, actor: ActorBaseInput) -> ActorOutput:
        """
        Create a new actor if it doesn't already exist in the database.

        Args:
            actor (ActorBaseInput): Actor information to create.

        Returns:
            ActorOutput: Created actor information.
        """
        if self.repository.actor_exists_by_full_name(actor.full_name):
            return self.repository.get_actor_by_full_name(actor.full_name)
        return self.repository.create_actor(actor)
