from pydantic import BaseModel
from datetime import datetime


class InvoiceCreate(BaseModel):
    subscription_id: int
    amount: float


class InvoiceResponse(BaseModel):
    id: int
    subscription_id: int
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True