from pydantic import BaseModel
from decimal import Decimal


class PlanCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    billing_interval: str
    trial_days: int
    features: str


class PlanUpdate(BaseModel):
    name: str
    description: str
    price: Decimal
    billing_interval: str
    trial_days: int
    features: str
    is_active: bool


class PlanResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    billing_interval: str
    trial_days: int
    features: str
    is_active: bool

    class Config:
        from_attributes = True