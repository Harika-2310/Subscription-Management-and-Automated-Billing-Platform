from pydantic import BaseModel
from datetime import date


class BillingCycleCreate(BaseModel):
    subscription_id: int
    billing_date: date
    next_billing_date: date


class BillingCycleResponse(BaseModel):
    id: int
    subscription_id: int
    billing_date: date
    next_billing_date: date
    status: str

    class Config:
        from_attributes = True