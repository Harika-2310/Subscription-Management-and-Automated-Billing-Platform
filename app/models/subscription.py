from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, Enum
import enum
from datetime import datetime
from app.database.base import Base


class SubscriptionStatus(enum.Enum):
    trial = "trial"
    active = "active"
    past_due = "past_due"
    cancelled = "cancelled"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)

    status = Column(
        Enum(SubscriptionStatus),
        default=SubscriptionStatus.trial,
        nullable=False
    )

    paused = Column(Boolean, default=False)

    cancel_at_period_end = Column(Boolean, default=False)

    start_date = Column(DateTime, default=datetime.utcnow)

    end_date = Column(DateTime)

    trial_end = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)