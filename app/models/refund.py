from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime
from datetime import datetime

from app.database.base import Base


class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    reason = Column(
        String(255)
    )

    status = Column(
        String(20),
        default="processed"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )