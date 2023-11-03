from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
)


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    total_amount = Column(Float(precision=2))

    to_be_paid = Column(Float(precision=2))

    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    is_signed = Column(Boolean())

    client_id = Column(Integer, ForeignKey("clients.id"))

    account_contact_id = Column(Integer, ForeignKey("employees.id"))

    client = relationship(
        "Client",
    )

    account_contact = relationship(
        "Employee",
    )

    HEADERS = (
        "id",
        "creation_date",
        "total_amount",
        "to_be_paid",
        "is_signed",
        "client_id",
        "account_contact_id",
    )

    def to_list(self):
        return (
            self.id,
            self.creation_date,
            self.total_amount,
            self.to_be_paid,
            self.is_signed,
            self.client_id,
            self.account_contact_id,
        )
