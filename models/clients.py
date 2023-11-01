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

    enterprise = Column(String(50))

    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    last_update = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    sales_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    sales_contact = relationship(
        "Employee",
    )

    def __repr__(self):
        return "\n".join(
            [
                f"id:            {self.id}",
                f"full name:     {self.full_name}",
                f"email:         {self.email}",
                f"phone:         {self.phone}",
                f"enterprise:    {self.enterprise}",
                f"creation date: {self.creation_date}",
                f"last update:   {self.last_update}",
                f"sales contact  {self.sales_contact_id}",
            ]
        )
