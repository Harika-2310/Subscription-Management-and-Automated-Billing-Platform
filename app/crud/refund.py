from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.refund import Refund
from app.models.invoice import Invoice


def create_refund(
    db: Session,
    invoice_id: int,
    refund_amount: Decimal,
    reason: str = "Subscription cancelled"
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        return None

    refund = Refund(
        invoice_id=invoice_id,
        amount=refund_amount,
        reason=reason,
        status="processed"
    )

    db.add(refund)

    # Mark invoice as refunded
    invoice.status = "refunded"

    db.commit()
    db.refresh(refund)

    return refund