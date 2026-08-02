from sqlalchemy import Column, Integer, Date, ForeignKey, String
from app.database.base import Base

class BillingCycle(Base):
    __tablename__ = "billing_cycles"

    id = Column(Integer, primary_key=True, index=True)

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id"),
        nullable=False
    )

    billing_date = Column(Date, nullable=False)

    next_billing_date = Column(Date, nullable=False)

    status = Column(String(20), default="pending")