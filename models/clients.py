from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from models import Base
from controller import utils


class Client(Base):
    __tablename__ = "clients"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    full_name = Column(String(50), nullable=False)

    email = Column(
        String(50),
        nullable=False,
        unique=True,
    )

    phone = Column(
        String(15),
        nullable=False,
        unique=True,
    )

    enterprise = Column(
        String(50)
    )

    creation_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    last_update = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    sales_contact_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )

    sales_contact = relationship(
        "Employee",
        cascade="all,delete",
    )

    HEADERS = (
        "id",
        "full_name",
        "email",
        "phone",
        "enterprise",
        "creation_date",
        "last_update",
        "sales_contact_id",
    )

    def to_list(self):
        return (
            self.id,
            self.full_name,
            self.email,
            self.phone,
            self.enterprise,
            self.creation_date,
            self.last_update,
            self.sales_contact_id,
        )

    @validates("email")
    def validate_email(self, key, value):
        return utils.validate_email(value)

    @validates("phone")
    def validate_phone(self, key, value):
        return utils.validate_phone(value)
