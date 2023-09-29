from models import Base
from sqlalchemy import (
    Enum,
    Column,
    Integer,
    String,
)
import enum


class Department(enum.Enum):
    SALES = "sales"
    ACCOUNTING = "accounting"
    SUPPORT = "support"


class Employee(Base):

    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    full_name = Column(
        String(50),
        nullable=False
    )

    email = Column(
        String(50),
        nullable=False,
        unique=True
    )

    password = Column(
        String(50),
        nullable=False
    )

    department = Column(
        Enum(Department),
        nullable=False
    )


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable
    print(CreateTable(Employee.__table__))
