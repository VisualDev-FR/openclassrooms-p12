import typing
from sqlalchemy.orm import Session
from datetime import datetime

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
    def create(
        self,
        start_date=datetime,
        end_date=datetime,
        location=str,
        attendees_count=int,
        notes=str,
        contract_id=int,
        support_contact_id=int,
    ):
        return super().create(
            Event(
                start_date=start_date,
                end_date=end_date,
                location=location,
                attendees_count=attendees_count,
                notes=notes,
                contract_id=contract_id,
                support_contact_id=support_contact_id,
            )
        )

    @login_required
    def get(self, *args, **kwargs) -> typing.List[Event]:
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Event]:
        return super().all()

    @permission_required([roles.ACCOUNTING, roles.SUPPORT])
    def update(self, where_clause, **values):
        return super().update(where_clause, **values)

    def delete(self, whereclause):
        raise PermissionError("Delete an event is forbidden.")
