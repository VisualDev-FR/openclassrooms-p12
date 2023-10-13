import pytest
from contextlib import contextmanager
from sqlalchemy.orm import Session
import sqlalchemy

from authentification.token import create_token, store_token, clear_token
from database.manager import DATABASE_PASSWORD, DATABASE_USERNAME
from models import Base
from models.employees import Employee, Department
from models.contracts import Contract
from models.clients import Client
from models.events import Event


__TEST_ENGINE = sqlalchemy.create_engine(
    f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/epicevents_test"
)


@pytest.fixture
def sales_employee() -> Employee:
    employee = Employee(
        full_name="sales, employee",
        email="sales.employee@epicevents.co",
        department=Department.SALES,
    )

    employee.set_password("password")
    return employee


@pytest.fixture
def account_employee() -> Employee:
    employee = Employee(
        full_name="account, employee",
        email="account.employee@epicevents.co",
        department=Department.ACCOUNTING,
    )

    employee.set_password("password")
    return employee


@pytest.fixture
def support_employee() -> Employee:
    employee = Employee(
        full_name="support, employee",
        email="support.employee@epicevents.co",
        department=Department.SUPPORT,
    )

    employee.set_password("password")
    return employee


@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(__TEST_ENGINE)
    yield
    Base.metadata.drop_all(__TEST_ENGINE)


@pytest.fixture(scope="function")
def session(setup_database, account_employee, sales_employee, support_employee):
    connection = __TEST_ENGINE.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    session.add_all([sales_employee, account_employee, support_employee])
    session.commit()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@contextmanager
def login_as_sales():
    try:
        token = create_token(user_id=1)
        store_token(token)
        yield

    finally:
        clear_token()


@contextmanager
def login_as_accounting():
    try:
        token = create_token(user_id=2)
        store_token(token)
        yield

    finally:
        clear_token()


@contextmanager
def login_as_support():
    try:
        token = create_token(user_id=3)
        store_token(token)
        yield
    finally:
        clear_token()
