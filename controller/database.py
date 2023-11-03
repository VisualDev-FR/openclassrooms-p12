from sqlalchemy.orm import Session
from contextlib import contextmanager
import sqlalchemy

from controller.environ import DATABASE_PASSWORD, DATABASE_USERNAME
from models import Base
from models.employees import Department, Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event

engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/EpicEvents"
)


@contextmanager
def create_session():
    try:
        connection = engine.connect()
        session = Session(bind=connection)

        yield session

    except PermissionError as e:
        print(e)

    except Exception as e:
        # TODO: handle exceptions here
        raise e

    finally:
        session.close()
        connection.close()


def drop_tables():
    """
    drop all database tables.
    """
    Base.metadata.drop_all(engine)


def create_tables():
    """
    create all database tables from the declared and imported models.
    """
    Base.metadata.create_all(engine)
