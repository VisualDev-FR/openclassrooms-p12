from abc import ABC
from sqlalchemy.orm import Session
from contextlib import contextmanager
import sqlalchemy
from tabulate import tabulate
from typing import List, Any

from authentification.environ import DATABASE_PASSWORD, DATABASE_USERNAME
from models import Base
from models.employees import Employee
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


class Manager(ABC):
    """
    class template to implement model managers.

    A model manager shall implement all CRUD methods to access or modify datas.
    """

    def __init__(self, session: Session, model: type) -> None:
        self._session = session
        self._model = model

    def create(self, obj):
        self._session.add(obj)
        self._session.commit()

        return obj

    def all(self):
        request = sqlalchemy.select(self._model)
        return self._session.scalars(request).all()

    def get(self, where_clause):
        request = sqlalchemy.select(self._model).where(where_clause)
        return self._session.scalars(request).all()

    def update(self, where_clause, **values):
        self._session.execute(
            sqlalchemy.update(self._model).where(where_clause).values(**values)
        )
        self._session.commit()

    def delete(self, whereclause):
        self._session.execute(sqlalchemy.delete(self._model).where(whereclause))
        self._session.commit()

    def tabulate(self, objects: List[Any], headers: List[str]) -> str:
        """
        Prettify a list of objects to a tabulated view.

        Args:
        * ``objects``: a list of objects to display, the objects must implement the method ``to_list()``
        * ``headers``: a list of strings containing the headers of the tabulated view

        Returns:
        A string representing the table of the given datas

        """
        return "\n" + tabulate(
            tabular_data=[obj.to_list() for obj in objects], headers=headers
        ) + "\n"
