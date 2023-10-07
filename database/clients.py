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

    def create(*args, **kwargs):
        return super().create(**kwargs)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Client]:
        return super().all()

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(*args, **kwargs):
        return super().delete(**kwargs)
