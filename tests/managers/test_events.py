from datetime import datetime
from sqlalchemy.orm import Session
import sqlalchemy
import pytest

from controller.managers import EventsManager
from models.events import Event


__DUMMY_EVENT = {
    "start_date": datetime(year=2023, month=10, day=27),
    "end_date": datetime(year=2023, month=10, day=28),
    "location": "Paris",
    "attendees_count": 5,
    "notes": "Nothing to note...",
    "contract_id": 1,
    "support_contact_id": 1,
}


@pytest.fixture(scope="function")
def event_manager(session):
    return EventsManager(session)


def test_create_event_from_authorized(event_manager: EventsManager, login_as_sales):

    with login_as_sales:
        event_manager.create(**__DUMMY_EVENT)
        created_event = event_manager.get(Event.location == "Paris")[0]

        assert created_event is not None
        assert created_event.notes == "Nothing to note..."


def test_create_event_from_unauthorized(event_manager: EventsManager, login_as_accounting, login_as_support):

    def create_event():
        event_manager.create(**__DUMMY_EVENT)
        created_event = event_manager.get(Event.location == "Paris")[0]

        assert created_event is not None
        assert created_event.notes == "Nothing to note..."

    with login_as_accounting, pytest.raises(PermissionError):
        create_event()

    with login_as_support, pytest.raises(PermissionError):
        create_event()


def test_get_all_events(event_manager: EventsManager, login_as_accounting, login_as_sales, login_as_support):
    def get_all_events():
        events = event_manager.all()
        assert len(events) == 1

    with login_as_accounting:
        get_all_events()

    with login_as_sales:
        get_all_events()

    with login_as_support:
        get_all_events()


def test_get_event(event_manager: EventsManager, login_as_accounting, login_as_sales, login_as_support):
    def get_event():
        events = event_manager.get(Event.location == "Dummy location")

        assert len(events) == 1
        assert events[0].attendees_count == 99

    with login_as_accounting:
        get_event()

    with login_as_sales:
        get_event()

    with login_as_support:
        get_event()


def test_update_event_from_authorized(event_manager: EventsManager):
    # TODO: test_update_event_from_authorized
    pass


def test_update_event_from_unauthorized(event_manager: EventsManager):
    # TODO: test_update_event_from_unauthorized
    pass


def test_delete_event_from_unauthorized(event_manager: EventsManager, login_as_sales):
    with login_as_sales, pytest.raises(PermissionError):
        event_manager.delete(Event.location == "Dummy location")


def test_delete_event_as_support_employee(session: Session, login_as_support):

    manager = EventsManager(session)

    def count_events() -> int:
        return len(session.scalars(sqlalchemy.select(Event)).all())

    with login_as_support:
        assert count_events() == 1

        manager.delete(Event.id == 1)

        assert count_events() == 0


def test_delete_event_as_accounting_employee(session: Session, login_as_accounting):

    manager = EventsManager(session)

    def count_events() -> int:
        return len(session.scalars(sqlalchemy.select(Event)).all())

    with login_as_accounting:
        assert count_events() == 1

        manager.delete(Event.id == 1)

        assert count_events() == 0
