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

    paid_at = Column(DateTime, default=datetime.utcnow)