import pytest
from contextlib import contextmanager
from sqlalchemy.orm import Session
import sqlalchemy
import datetime

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


# -----------------------------------
# database test datas
# -----------------------------------
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


@pytest.fixture
def client() -> Client:
    return Client(
        sales_contact_id=1,
        email="first.client@example.co",
        full_name="First, Client",
        phone="0607080910",
        enterprise="First Client Enterprise",
    )


@pytest.fixture
def contract() -> Contract:
    return Contract(
        client_id=1,
        account_contact_id=2,
        total_amount=99.9,
        to_be_paid=99.9,
        is_signed=False,
    )


@pytest.fixture
def event() -> Event:
    return Event(
        start_date=datetime.datetime(year=2050, month=11, day=17),
        end_date=datetime.datetime(year=2050, month=11, day=17),
        location="Dummy location",
        attendees_count=99,
        notes="Dummies notes",
        support_contact_id=3,
        contract_id=1,
    )


# -----------------------------------
# database setup
# -----------------------------------
@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(__TEST_ENGINE)
    yield
    Base.metadata.drop_all(__TEST_ENGINE)


@pytest.fixture(scope="function")
def session(
    setup_database,
    account_employee,
    sales_employee,
    support_employee,
    client,
    contract,
    event,
):
    connection = __TEST_ENGINE.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    session.add_all(
        [sales_employee, account_employee, support_employee, client, contract, event]
    )
    session.commit()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# -----------------------------------
# login fixtures
# -----------------------------------
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
