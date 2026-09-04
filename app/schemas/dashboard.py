from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class FailedPaymentResponse(BaseModel):
    id: int
    invoice_id: int
    amount: Decimal
    payment_method: str | None
    retry_count: int
    next_retry_at: datetime | None
    last_attempt_at: datetime | None
    status: str

    class Config:
        from_attributes = True