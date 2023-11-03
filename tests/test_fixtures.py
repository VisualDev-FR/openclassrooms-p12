from tests.conftest import login_as_accounting, login_as_sales, login_as_support
from controller.authentification import retreive_token, decode_token
from models.employees import Employee, Department
from models.clients import Client
from models.contracts import Contract
from models.events import Event
import sqlalchemy
from sqlalchemy.orm import Session


def test_login_fixtures(session: Session):
    """
    Check that all login fixtures have the expected behavior
    """

    # login as accounting user
    with login_as_accounting():
        token = retreive_token()
        payload = decode_token(token)

        authenticated_user_id = payload["user_id"]

        request = sqlalchemy.select(Employee).where(
            Employee.id == authenticated_user_id
        )
        # assert len(session.scalars(request).all()) == 1
        assert session.scalars(request).first(
        ).department == Department.ACCOUNTING
    assert retreive_token() is None

    # login as sales
    with login_as_sales():
        token = retreive_token()
        payload = decode_token(token)

        authenticated_user_id = payload["user_id"]

        request = sqlalchemy.select(Employee).where(
            Employee.id == authenticated_user_id
        )
        assert len(session.scalars(request).all()) == 1
        assert session.scalars(request).first().department == Department.SALES
    assert retreive_token() is None

    # login as support
    with login_as_support():
        token = retreive_token()
        payload = decode_token(token)

        authenticated_user_id = payload["user_id"]

        request = sqlalchemy.select(Employee).where(
            Employee.id == authenticated_user_id
        )
        assert len(session.scalars(request).all()) == 1
        assert session.scalars(request).first(
        ).department == Department.SUPPORT
    assert retreive_token() is None


def test_database_fixtures(session: Session):
    """
    Check that all desired datas are present in the test database
    """

    request = sqlalchemy.select(Employee)
    assert len(session.scalars(request).all()) == 3

    # check sales user
    request = sqlalchemy.select(Employee).where(
        Employee.department == Department.SALES)
    assert session.scalars(request).first().id == 1

    # check accounting user
    request = sqlalchemy.select(Employee).where(
        Employee.department == Department.ACCOUNTING
    )
    assert session.scalars(request).first().id == 2

    # check support user
    request = sqlalchemy.select(Employee).where(
        Employee.department == Department.SUPPORT
    )
    assert session.scalars(request).first().id == 3

    # check first client
    request = sqlalchemy.select(Client)
    assert session.scalars(request).first().id == 1

    # check first contract
    request = sqlalchemy.select(Contract)
    assert session.scalars(request).first().id == 1

    # check first event
    request = sqlalchemy.select(Event)
    assert session.scalars(request).first().id == 1
