import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


def create_engine(username: str, password: str, host: str = "localhost") -> sqlalchemy.Engine:
    return sqlalchemy.create_engine(f'mysql+pymysql://{username}:{password}@{host}/EpicEvents')
