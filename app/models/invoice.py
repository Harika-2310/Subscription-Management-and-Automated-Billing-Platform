from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from datetime import datetime

from app.database.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id"),
        nullable=False
    )
    country = Column(
    String(10),
    nullable=False,
    default="IN"
    )

    region = Column(
    String(50),
    nullable=True
    )

    plan_fee = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    proration_amount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    usage_charges = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    tax_rate = Column(
        Numeric(5, 2),
        nullable=False,
        default=18
    )

    tax = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    total = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    status = Column(
        String(20),
        default="pending",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )