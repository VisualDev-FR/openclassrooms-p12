import typing
from sqlalchemy.orm import Session
from database.manager import Manager
from models.events import Event
from models.employees import Department as roles
from authentification.decorators import login_required, permission_required


class EventsManager(Manager):
    """
    Manage the access to ``Event`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Event)

    @permission_required([roles.SALES])
    def create(*args, **kwargs):
        return super().create(**kwargs)

    @login_required
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Event]:
        return super().all()

    @permission_required([roles.ACCOUNTING, roles.SUPPORT])
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(*args, **kwargs):
        return super().delete(**kwargs)
