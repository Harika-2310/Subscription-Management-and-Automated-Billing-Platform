from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime

from app.database.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    amount = Column(Float, nullable=False)

    payment_method = Column(String(50))

    status = Column(String(20), default="pending")

    paid_at = Column(DateTime, nullable=True)

    # Week 5-6: Failed payment retry
    retry_count = Column(Integer, default=0)

    next_retry_at = Column(DateTime, nullable=True)

    last_attempt_at = Column(DateTime, nullable=True)

    # Original payment failure time
    original_failure_at = Column(
        DateTime,
        nullable=True
    )