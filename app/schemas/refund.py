from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class RefundCreate(BaseModel):
    invoice_id: int
    refund_amount: Decimal
    reason: str = "Subscription cancelled"


class RefundResponse(BaseModel):
    id: int
    invoice_id: int
    amount: Decimal
    reason: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True