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

    contract_id = Column(Integer, ForeignKey("contracts.id"))

    support_contact_id = Column(Integer, ForeignKey("employees.id"))

    contract = relationship("Contract")

    support_contact = relationship(
        "Employee",
    )

    def __repr__(self):
        return "\n".join(
            [
                f"id:                 {self.id}",
                f"creation_date:      {self.creation_date}",
                f"start_date:         {self.start_date}",
                f"end_date:           {self.end_date}",
                f"location:           {self.location}",
                f"attendees_count:    {self.attendees_count}",
                f"notes:              {self.notes}",
                f"contract_id:        {self.contract_id}",
                f"support_contact_id: {self.support_contact_id}",
            ]
        )
