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

    def create(*args, **kwargs):
        return super().create(**kwargs)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Event]:
        return super().all()

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(*args, **kwargs):
        return super().delete(**kwargs)
