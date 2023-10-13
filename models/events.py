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

    support_contact_id = Column(Integer, ForeignKey("employees.id"))

    support_contact = relationship(
        "Employee",
    )
