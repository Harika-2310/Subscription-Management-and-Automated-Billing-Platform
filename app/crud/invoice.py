from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.invoice_tax_item import InvoiceTaxItem
from sqlalchemy import func
from app.models.invoice_tax_item import InvoiceTaxItem
from app.models.invoice import Invoice
from app.models.subscription import Subscription
from app.models.plan import Plan

from app.services.invoice_service import calculate_invoice


def create_invoice(
    db: Session,
    subscription_id: int,
    usage_charges: Decimal = Decimal("0.00"),
    country: str = "IN",
    region: str = None
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
        country=country,
        region=region
    )

    # Create database record
    invoice = Invoice(
        invoice_number=invoice_data["invoice_number"],
        subscription_id=subscription_id,

        country=invoice_data["country"],
        region=invoice_data["region"],

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
    # Create tax line item
    tax_item = InvoiceTaxItem(
        invoice_id=invoice.id,
        country=invoice.country,
        region=invoice.region,
        tax_rate=invoice.tax_rate,
        tax_amount=invoice.tax
    )   

    db.add(tax_item)
    db.commit()

    return invoice
def get_tax_report(db: Session):
    """
    Get total tax collected grouped by country and region.
    """

    results = db.query(
        InvoiceTaxItem.country,
        InvoiceTaxItem.region,
        func.sum(InvoiceTaxItem.tax_amount).label("total_tax")
    ).group_by(
        InvoiceTaxItem.country,
        InvoiceTaxItem.region
    ).all()

    return [
        {
            "country": row.country,
            "region": row.region,
            "total_tax": row.total_tax
        }
        for row in results
    ]