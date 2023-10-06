from sqlalchemy.orm import Session
import sqlalchemy

from authentification.environ import DATABASE_PASSWORD
from models import Base
from models.employees import Employee
# from models.clients import Client
# from models.contracts import Contract
# from models.events import Event


def create_engine() -> sqlalchemy.Engine:
    if DATABASE_PASSWORD:
        # TODO: change root user
        return sqlalchemy.create_engine(
            f"mysql+pymysql://root:{DATABASE_PASSWORD}@localhost/EpicEvents"
        )

    else:
        raise AttributeError("Environnement variable not set : EPICEVENTS_PW")


def create_tables():
    # create sqlAlchemy engine
    engine = create_engine()

    # create all database tables
    Base.metadata.create_all(engine)


engine = create_engine()


if __name__ == "__main__":
    create_tables()
