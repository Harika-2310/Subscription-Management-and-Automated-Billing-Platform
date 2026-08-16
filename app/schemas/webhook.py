from pydantic import BaseModel


class PaymentWebhook(BaseModel):
    event: str
    payment_id: int
    invoice_id: int