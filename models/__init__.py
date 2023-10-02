import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()


def create_engine() -> sqlalchemy.Engine:

    password = os.environ.get("EPICEVENTS_PW")
    password = "root"

    if password:
        return sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/EpicEvents')

    else:
        raise AttributeError("Environnement variable not set : EPICEVENTS_PW")
