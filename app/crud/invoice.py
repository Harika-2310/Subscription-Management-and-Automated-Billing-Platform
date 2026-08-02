from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate


def create_invoice(db: Session, invoice: InvoiceCreate):

    db_invoice = Invoice(
        subscription_id=invoice.subscription_id,
        amount=invoice.amount,
        status="pending"
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    return db_invoice