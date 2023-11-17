import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session
import sqlalchemy

from models import Base
from models.employees import Employee, Department
from models.contracts import Contract
from models.clients import Client
from models.events import Event
from controller.environ import DATABASE_PASSWORD, DATABASE_USERNAME
from view.init_database import create_employees, create_clients, create_contracts, create_events

__TEST_ENGINE = sqlalchemy.create_engine(
    f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/epicevents_test"
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
def session(setup_database):
    """
    DOCME
    """

    connection = __TEST_ENGINE.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    create_employees(session)
    create_clients(session)
    create_contracts(session)
    create_events(session)

    session.commit()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def database_mock(session):
    return patch("controller.database.create_session", return_value=session)


# -----------------------------------
# login fixtures
# -----------------------------------

@pytest.fixture
def login_as_sales():
    return patch("controller.authentification.get_authenticated_user_id", return_value=1)


@pytest.fixture
def login_as_accounting():
    return patch("controller.authentification.get_authenticated_user_id", return_value=2)


@pytest.fixture
def login_as_support():
    return patch("controller.authentification.get_authenticated_user_id", return_value=3)


# -----------------------------------
# click fixtures
# -----------------------------------

@pytest.fixture
def force_click_confirm():
    return patch("click.confirm", return_value="y")
