from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from sqlalchemy import Enum, Column, Integer, String, DateTime
from typing import List
import enum
import bcrypt

from controller import utils
from models import Base


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
        from controller import authentification as auth
        self.password_hash, self.salt = auth.encrypt_password(password)

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

    @validates("email")
    def validate_email(self, key, value):
        return utils.validate_email(value)
