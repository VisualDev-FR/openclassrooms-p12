import typing
from sqlalchemy.orm import Session
from database.manager import Manager
from models.clients import Client
from authentification.decorators import login_required


class ClientsManager(Manager):
    """
    Manage the access to ``Client`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Client)

    @login_required
    def all(self) -> typing.List[Client]:
        return super().all()
