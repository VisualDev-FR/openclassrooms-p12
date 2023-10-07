import typing
from sqlalchemy.orm import Session
from database.manager import Manager
from models.contracts import Contract
from authentification.decorators import login_required


class EventsManager(Manager):
    """
    Manage the access to ``Contract`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Contract)

    @login_required
    def all(self) -> typing.List[Contract]:
        return super().all()
