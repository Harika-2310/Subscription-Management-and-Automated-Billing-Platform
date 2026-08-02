from pydantic import BaseModel
from datetime import datetime


class PaymentCreate(BaseModel):
    invoice_id: int
    amount: float
    payment_method: str


class PaymentResponse(BaseModel):
    id: int
    invoice_id: int
    amount: float
    payment_method: str
    status: str
    paid_at: datetime

    class Config:
        from_attributes = True