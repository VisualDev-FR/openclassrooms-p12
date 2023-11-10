from models import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum, Column, Integer, String, DateTime
import enum
import bcrypt
from typing import List


class Department(enum.Enum):
    SALES = "sales"
    ACCOUNTING = "accounting"
    SUPPORT = "support"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)

    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    full_name = Column(String(50), nullable=False)

    email = Column(String(50), nullable=False, unique=True)

    password_hash = Column(String(60), nullable=False)

    salt = Column(String(30), nullable=False)

    department = Column(Enum(Department), nullable=False)

    last_update = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    def set_password(self, password: str):
        """
        Hash and store a new password + salt value
        """
        # generate new salt
        salt = bcrypt.gensalt()

        # hash password with generated salt
        password_hash = bcrypt.hashpw(password=password.encode("utf-8"), salt=salt)

        # set the hashed password and the salt value
        self.password_hash = password_hash.decode("utf-8")
        self.salt = salt.decode("utf-8")

    def check_password(self, password: str) -> bool:
        """
        Allow to check if a given password is valid, regarding the registered password
        """
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=self.password_hash.encode("utf-8"),
        )

    HEADERS = ["id", "creation_date", "email", "full_name", "department"]

    def to_list(self):
        return (
            self.id,
            self.creation_date,
            self.email,
            self.full_name,
            self.department.name,
        )
