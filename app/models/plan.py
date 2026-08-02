from sqlalchemy import Column, Integer, String, Numeric, Boolean
from app.database.base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False, unique=True)

    description = Column(String(500))

    price = Column(Numeric(10, 2), nullable=False)

    billing_interval = Column(String(20), nullable=False)   # monthly / annual

    trial_days = Column(Integer, default=0)

    features = Column(String(1000))

    is_active = Column(Boolean, default=True)