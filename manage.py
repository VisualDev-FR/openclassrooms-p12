from models import Base, create_engine
from models.clients import Client
from models.employees import Employee
from models.contracts import Contract
from models.events import Event


def create_tables():
    # create sqlAlchemy engine
    engine = create_engine()

    # create all database tables
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
