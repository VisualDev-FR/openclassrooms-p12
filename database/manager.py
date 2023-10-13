from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import sqlalchemy
import typing

from authentification.environ import DATABASE_PASSWORD, DATABASE_USERNAME
from models import Base
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event


engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/EpicEvents"
)


engine_test = sqlalchemy.create_engine(
    f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/epicevents_test"
)


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


class Manager(ABC):
    """
    class template to implement model managers.

    A model manager shall implement all CRUD methods to access or modify datas.
    """

    def __init__(self, session: Session, model: type) -> None:
        self._session = session
        self._model = model

    def create(self, obj):
        try:
            self._session.add(obj)
            self._session.commit()

            return obj

        except IntegrityError as e:
            print(f"Integrity error : {e._message()}")

        except Exception as e:
            print(f"Unhandled exception: {type(e).__name__}")

        return None

    def all(self):
        request = sqlalchemy.select(self._model)
        return [obj for obj in self._session.scalars(request)]

    def get(self, where_clause):
        request = sqlalchemy.select(self._model).where(where_clause)
        return [obj for obj in self._session.scalars(request)]

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(*args, **kwargs):
        pass
