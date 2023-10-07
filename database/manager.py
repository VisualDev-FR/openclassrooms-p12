import sqlalchemy

from authentification.environ import DATABASE_PASSWORD, DATABASE_USERNAME
from models.employees import Employee
from models import Base

# from models.clients import Client
# from models.contracts import Contract
# from models.events import Event


engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/EpicEvents"
)


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
