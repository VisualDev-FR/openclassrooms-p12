import pytest
from database.manager import engine_test
from models.clients import Client
from models.contracts import Contract
from models.employees import Employee, Department
from models.events import Event
from models import Base
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from unittest.mock import patch


@pytest.fixture(scope="session")
def setup_database():
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)


@pytest.fixture
def account_employee():
    employee = Employee(
        full_name="account, employee",
        email="account.employee@epicevents.co",
        department=Department.ACCOUNTING,
    )

    employee.set_password("password")
    return employee


@pytest.fixture
def sales_employee():
    employee = Employee(
        full_name="sales, employee",
        email="sales.employee@epicevents.co",
        department=Department.SALES,
    )

    employee.set_password("password")
    return employee


@pytest.fixture
def support_employee():
    employee = Employee(
        full_name="support, employee",
        email="support.employee@epicevents.co",
        department=Department.SUPPORT,
    )

    employee.set_password("password")
    return employee


@pytest.fixture
def session(setup_database, account_employee, sales_employee, support_employee):
    connection = engine_test.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    session.add_all([sales_employee, account_employee, support_employee])
    session.commit()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
