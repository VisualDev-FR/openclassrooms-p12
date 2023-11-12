from controller.authentification import retreive_token, decode_token
from models.employees import Employee, Department
from models.clients import Client
from models.contracts import Contract
from models.events import Event
import sqlalchemy
from sqlalchemy.orm import Session


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
