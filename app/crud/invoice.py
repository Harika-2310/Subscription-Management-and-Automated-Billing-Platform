from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.invoice import Invoice
from app.models.subscription import Subscription
from app.models.plan import Plan

from app.services.invoice_service import calculate_invoice


def create_invoice(
    db: Session,
    subscription_id: int,
    usage_charges: Decimal = Decimal("0.00")
):
    # Find subscription
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    # Find plan
    plan = db.query(Plan).filter(
        Plan.id == subscription.plan_id
    ).first()

    if not plan:
        return None

    # Calculate invoice
    invoice_data = calculate_invoice(
        plan_fee=Decimal(str(plan.price)),
        proration_amount=Decimal("0.00"),
        usage_charges=usage_charges,
        tax_rate=Decimal("18.00")
    )

    # Create database record
    invoice = Invoice(
        invoice_number=invoice_data["invoice_number"],
        subscription_id=subscription_id,
        plan_fee=invoice_data["plan_fee"],
        proration_amount=invoice_data["proration_amount"],
        usage_charges=invoice_data["usage_charges"],
        subtotal=invoice_data["subtotal"],
        tax_rate=invoice_data["tax_rate"],
        tax=invoice_data["tax"],
        total=invoice_data["total"],
        status="pending"
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice