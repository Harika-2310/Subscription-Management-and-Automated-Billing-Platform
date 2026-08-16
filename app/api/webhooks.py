from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.webhook import PaymentWebhook

from app.models.payment import Payment
from app.models.invoice import Invoice
from app.models.subscription import Subscription


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)


@router.post("/payment")
def payment_webhook(
    webhook: PaymentWebhook,
    db: Session = Depends(get_db)
):

    payment = db.query(Payment).filter(
        Payment.id == webhook.payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    invoice = db.query(Invoice).filter(
        Invoice.id == webhook.invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    subscription = db.query(Subscription).filter(
        Subscription.id == invoice.subscription_id
    ).first()

    if webhook.event == "paid":

        payment.status = "paid"
        invoice.status = "paid"

        if subscription and subscription.status == "trial":
            subscription.status = "active"

        message = "Payment received successfully"

    elif webhook.event == "failed":

        payment.status = "failed"
        invoice.status = "failed"

        if subscription:
            subscription.status = "past_due"

        message = "Payment failed"

    elif webhook.event == "refunded":

        payment.status = "refunded"
        invoice.status = "refunded"

        message = "Payment refunded"

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment event"
        )

    db.commit()

    return {
        "message": message,
        "event": webhook.event,
        "payment_id": payment.id,
        "invoice_id": invoice.id
    }