import typing
from sqlalchemy.orm import Session
from database.manager import Manager
from models.events import Event
from authentification.decorators import login_required


class EventsManager(Manager):
    """
    Manage the access to ``Event`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Event)

    @login_required
    def all(self) -> typing.List[Event]:
        return super().all()
