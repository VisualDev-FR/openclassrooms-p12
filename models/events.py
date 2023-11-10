from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)

    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    start_date = Column(DateTime())

    end_date = Column(DateTime())

    location = Column(String(50))

    attendees_count = Column(Integer())

    notes = Column(String(1000))

    contract_id = Column(
        Integer,
        ForeignKey("contracts.id", ondelete="CASCADE"),
    )

    support_contact_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
    )

    contract = relationship(
        "Contract",
        cascade="all,delete",
    )

    support_contact = relationship(
        "Employee",
        cascade="all,delete",
    )

    HEADERS = (
        "id",
        "creation_date",
        "start_date",
        "end_date",
        "location",
        "attendees_count",
        "notes",
        "contract_id",
        "support_contact_id",
    )

    def to_list(self):
        return (
            self.id,
            self.creation_date,
            self.start_date,
            self.end_date,
            self.location,
            self.attendees_count,
            self.notes,
            self.contract_id,
            self.support_contact_id,
        )
