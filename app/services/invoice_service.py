from decimal import Decimal
from datetime import datetime


def calculate_invoice(
    plan_fee: Decimal,
    proration_amount: Decimal = Decimal("0.00"),
    usage_charges: Decimal = Decimal("0.00"),
    tax_rate: Decimal = Decimal("18.00")
):
    subtotal = (
        plan_fee
        + proration_amount
        + usage_charges
    )

    tax = subtotal * tax_rate / Decimal("100")

    total = subtotal + tax

    invoice_number = (
        f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
    )

    return {
        "invoice_number": invoice_number,
        "plan_fee": plan_fee.quantize(Decimal("0.01")),
        "proration_amount": proration_amount.quantize(Decimal("0.01")),
        "usage_charges": usage_charges.quantize(Decimal("0.01")),
        "subtotal": subtotal.quantize(Decimal("0.01")),
        "tax_rate": tax_rate,
        "tax": tax.quantize(Decimal("0.01")),
        "total": total.quantize(Decimal("0.01"))
    }