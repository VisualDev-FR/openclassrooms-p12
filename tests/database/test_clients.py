import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from database.clients import ClientsManager
from models.clients import Client
from tests.conftest import login_as_accounting, login_as_sales, login_as_support


def test_create_client_from_sales_employee(session):
    """
    Check that sales employees are allowed to create a new client
    """

    manager = ClientsManager(session)

    with login_as_sales():
        created_client = manager.create(
            email="dummy.client@example.co",
            full_name="Dummy, Client",
            phone="0607080910",
            enterprise="dummy enterprise",
            sales_contact_id=1,
        )

        assert created_client is not None

        created_client = manager.get(Client.full_name == "Dummy, Client")[0]

        assert created_client.id == 1
