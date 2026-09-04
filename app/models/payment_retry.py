from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.database.base import Base


class PaymentRetry(Base):
    __tablename__ = "payment_retries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    payment_id = Column(
        Integer,
        ForeignKey("payments.id"),
        nullable=False
    )

    attempt_number = Column(
        Integer,
        nullable=False
    )

    scheduled_at = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String(20),
        default="pending",
        nullable=False
    )

    attempted_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )