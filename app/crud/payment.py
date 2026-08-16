from sqlalchemy.orm import Session
from datetime import datetime

from app.models.payment import Payment
from app.models.invoice import Invoice
from app.services.payment_service import process_payment


def create_payment(
    db: Session,
    invoice_id: int,
    amount: float,
    payment_method: str,
    success_rate: int = 80
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        return None

    result = process_payment(
        amount=amount,
        success_rate=success_rate
    )

    payment = Payment(
        invoice_id=invoice_id,
        amount=amount,
        payment_method=payment_method,
        status=result["status"],
        paid_at=(
            datetime.utcnow()
            if result["status"] == "paid"
            else None
        )
    )

    db.add(payment)

    # Update invoice status
    if result["status"] == "paid":
        invoice.status = "paid"
    else:
        invoice.status = "failed"

    db.commit()
    db.refresh(payment)

    return payment