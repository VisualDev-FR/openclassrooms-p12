from sqlalchemy.orm import Session
import sqlalchemy
import pytest

from controller.cascade import CascadeResolver
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract


@pytest.fixture(scope="function")
def resolver(session):
    return CascadeResolver(session)


def retreive_object(model: type, id: int, session: Session):
    return session.scalars(
        sqlalchemy.select(model)
        .where(model.id == id)
    ).all()


def test_retreive_clients_from_employees(database_mock, session, resolver: CascadeResolver):

    with database_mock:

        retreived_clients = resolver._retreive_clients_from_employees(
            employees=retreive_object(
                model=Employee,
                id=1,
                session=session,
            )
        )

        assert len(retreived_clients) == 3
        assert retreived_clients[0].email == "alice.johnson@example.com"
        assert retreived_clients[1].email == "ella.davis@example.com"
        assert retreived_clients[2].email == "isabella.adams@example.com"


def test_retreive_contracts_from_employees(database_mock, session, resolver: CascadeResolver):

    with database_mock:

        retreived_contracts = resolver._retreive_contracts_from_employees(
            employees=retreive_object(
                model=Employee,
                id=2,
                session=session,
            )
        )

        assert len(retreived_contracts) == 4
        assert retreived_contracts[0].total_amount == 5000
        assert retreived_contracts[1].total_amount == 10000
        assert retreived_contracts[2].total_amount == 4500
        assert retreived_contracts[3].total_amount == 9500


def test_retreive_events_from_employee(database_mock, session, resolver: CascadeResolver):

    with database_mock:

        retreived_events = resolver._retreive_events_from_employee(
            employees=retreive_object(
                model=Employee,
                id=3,
                session=session,
            )
        )

        assert len(retreived_events) == 4
        assert retreived_events[0].location == "Salle A"
        assert retreived_events[1].location == "Salle D"
        assert retreived_events[2].location == "Salle G"
        assert retreived_events[3].location == "Salle de réunion J"


def test_retreive_contracts_from_clients(database_mock, session, resolver: CascadeResolver):

    with database_mock:

        retreived_contracts = resolver._retreive_contracts_from_clients(
            clients=retreive_object(
                model=Client,
                id=3,
                session=session,
            )
        )

        assert len(retreived_contracts) == 1
        assert retreived_contracts[0].total_amount == 3000


def test_retreive_events_from_contracts(database_mock, session, resolver: CascadeResolver):

    with database_mock:

        retreived_events = resolver._retreive_events_from_contracts(
            contracts=retreive_object(
                model=Contract,
                id=1,
                session=session,
            )
        )

        assert len(retreived_events) == 1
        assert retreived_events[0].location == "Salle A"


def test_resolve_employee_cascade(database_mock, session, resolver: CascadeResolver):

    with database_mock:

        details = resolver.resolve_employee_cascade(
            employees=retreive_object(
                model=Employee,
                id=1,
                session=session,
            )
        )

        assert len(details) == 4

        assert details[0].objects[0].email == "sales.employee@epicevents.co"
        assert details[1].objects[0].email == "alice.johnson@example.com"
        assert details[2].objects[1].total_amount == 6000
        assert details[3].objects[1].location == "Salle E"


def test_resolve_clients_cascade(database_mock, session, resolver: CascadeResolver):

    with database_mock:

        details = resolver.resolve_clients_cascade(
            clients=retreive_object(
                model=Client,
                id=1,
                session=session,
            )
        )

        assert len(details) == 3

        assert details[0].objects[0].email == "alice.johnson@example.com"
        assert details[1].objects[0].total_amount == 5000
        assert details[2].objects[0].location == "Salle A"


def test_resolve_contract_cascade(database_mock, session, resolver: CascadeResolver):

    with database_mock:

        details = resolver.resolve_contracts_cascade(
            contracts=retreive_object(
                model=Contract,
                id=1,
                session=session,
            )
        )

        assert len(details) == 2

        assert details[0].objects[0].total_amount == 5000
        assert details[1].objects[0].location == "Salle A"
