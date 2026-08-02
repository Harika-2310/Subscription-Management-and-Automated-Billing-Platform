from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate


def make_payment(db: Session, payment: PaymentCreate):

    db_payment = Payment(
        invoice_id=payment.invoice_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status="paid"
    )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment