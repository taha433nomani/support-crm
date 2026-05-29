from sqlalchemy import Column, Integer, String
from database import Base

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)

    customer_email = Column(String, nullable=False)

    subject = Column(String, nullable=False)

    description = Column(String, nullable=False)

    status = Column(String, default="Open")

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )