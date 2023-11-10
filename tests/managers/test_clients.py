import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from tests.conftest import login_as_accounting, login_as_sales, login_as_support
from controller.managers import ClientsManager
from models.clients import Client
from models.contracts import Contract
from models.events import Event


DUMMY_CLIENT = {
    "email": "dummy.client@example.co",
    "full_name": "Dummy, Client",
    "phone": "0607080911",
    "enterprise": "dummy enterprise",
    "sales_contact_id": 1,
}

CLIENT_EMAIL = "first.client@example.co"


def test_create_client_from_sales_employee(session: Session):
    """
    Check that sales employees are allowed to create a new client
    """

    manager = ClientsManager(session)

    with login_as_sales():
        created_client = manager.create(**DUMMY_CLIENT)

        assert created_client is not None

        created_client = manager.get(
            Client.full_name == DUMMY_CLIENT["full_name"])[0]

        assert created_client.email == DUMMY_CLIENT["email"]


def test_create_employee_from_unauthorized(session: Session):
    """
    check that sales or support employees are not allowed to create a new employee
    """

    manager = ClientsManager(session)

    with login_as_accounting(), pytest.raises(PermissionError):
        manager.create(**DUMMY_CLIENT)

    with login_as_support(), pytest.raises(PermissionError):
        manager.create(**DUMMY_CLIENT)

    request = sqlalchemy.select(Client).where(
        Client.full_name == DUMMY_CLIENT["full_name"]
    )
    assert session.scalars(request).all() == []


def test_get_all_clients(session: Session):
    """
    check thaht all clients can be accessed from all users
    """

    manager = ClientsManager(session)

    with login_as_accounting():
        assert len(manager.all()) == 1

    with login_as_sales():
        assert len(manager.all()) == 1

    with login_as_support():
        assert len(manager.all()) == 1


def test_get_client(session):
    """
    check that employees can be searched from all users
    """

    manager = ClientsManager(session)

    with login_as_accounting():
        client = manager.get(Client.email == CLIENT_EMAIL)[0]
        assert client.id == 1

    with login_as_sales():
        client = manager.get(Client.email == CLIENT_EMAIL)[0]
        assert client.id == 1

    with login_as_support():
        client = manager.get(Client.email == CLIENT_EMAIL)[0]
        assert client.id == 1


def test_delete_client(session: Session):
    """
    Check that no user is allowed to delete a client.
    """

    manager = ClientsManager(session)

    def count_all_contracts() -> int:
        return len(session.scalars(sqlalchemy.select(Contract)).all())

    def count_all_events() -> int:
        return len(session.scalars(sqlalchemy.select(Event)).all())

    with login_as_sales():

        assert count_all_contracts() == 1
        assert count_all_events() == 1

        manager.delete(Client.email == CLIENT_EMAIL)

        assert count_all_contracts() == 0
        assert count_all_events() == 0


def test_delete_client_from_unauthorized(session):
    """
    Check that no user is allowed to delete a client.
    """

    manager = ClientsManager(session)

    def delete_client():
        manager.delete(Client.email == CLIENT_EMAIL)

    with login_as_accounting(), pytest.raises(PermissionError):
        delete_client()

    with login_as_support(), pytest.raises(PermissionError):
        delete_client()


def test_update_client_from_sales_employee(session):
    manager = ClientsManager(session)

    with login_as_sales():
        manager.update(
            where_clause=Client.email == "first.client@example.co",
            full_name="updated_client_fullname",
        )

        assert (
            manager.get(Client.email == "first.client@example.co")[0].full_name
            == "updated_client_fullname"
        )


def test_update_client_from_unauthorized(session):
    manager = ClientsManager(session)

    def update_client():
        manager.update(
            where_clause=Client.email == "first.client@example.co",
            full_name="updated_client_fullname",
        )

    with login_as_accounting(), pytest.raises(PermissionError):
        update_client()

    with login_as_support(), pytest.raises(PermissionError):
        update_client()
