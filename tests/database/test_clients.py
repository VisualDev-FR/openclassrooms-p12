import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from database.clients import ClientsManager
from models.clients import Client
from tests.conftest import login_as_accounting, login_as_sales, login_as_support


DUMMY_CLIENT = {
    "email": "dummy.client@example.co",
    "full_name": "Dummy, Client",
    "phone": "0607080911",
    "enterprise": "dummy enterprise",
    "sales_contact_id": 1,
}


def test_create_client_from_sales_employee(session: Session):
    """
    Check that sales employees are allowed to create a new client
    """

    manager = ClientsManager(session)

    with login_as_sales():
        created_client = manager.create(**DUMMY_CLIENT)

        assert created_client is not None

        created_client = manager.get(Client.full_name == DUMMY_CLIENT["full_name"])[0]

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
