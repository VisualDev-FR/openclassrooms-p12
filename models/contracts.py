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

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    total_amount = Column(
        Float(precision=2)
    )

    to_be_paid = Column(
        Float(precision=2)
    )

    creation_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    is_signed = Column(
        Boolean()
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id")
    )

    account_contact_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id")
    )

    client = relationship(
        "Client",
        back_populates="contracts"
    )

    account_contact = relationship(
        "Employee",
        back_populates="contracts"
    )

    event = relationship(
        "Event",
        back_populates="contracts"
    )
