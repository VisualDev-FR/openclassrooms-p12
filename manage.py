from sqlalchemy.orm import Session
from models import Base, create_engine
from models.clients import Client
from models.employees import Employee


def create_tables():
    # create sqlAlchemy engine
    engine = create_engine(username='root', password='lW.5K4~GWBWeJk/$n,1`')

    # create SQLAlchemy session
    session = Session(engine)

    # create all database tables
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
