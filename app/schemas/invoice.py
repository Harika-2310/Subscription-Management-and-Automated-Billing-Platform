from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class InvoiceCreate(BaseModel):
    subscription_id: int
    usage_charges: Decimal = Decimal("0.00")
    country: str = "IN"
    region: str | None = None

class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    subscription_id: int
    country: str
    region: str | None
    plan_fee: Decimal
    proration_amount: Decimal
    usage_charges: Decimal
    subtotal: Decimal
    tax_rate: Decimal
    tax: Decimal
    total: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
class TaxReportResponse(BaseModel):
    country: str
    region: str | None
    total_tax: Decimal