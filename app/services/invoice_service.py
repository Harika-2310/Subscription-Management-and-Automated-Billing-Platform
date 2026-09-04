from decimal import Decimal
from datetime import datetime

from app.services.tax_service import calculate_tax


def calculate_invoice(
    plan_fee: Decimal,
    proration_amount: Decimal = Decimal("0.00"),
    usage_charges: Decimal = Decimal("0.00"),
    country: str = "IN",
    region: str = None
):
    subtotal = (
        plan_fee
        + proration_amount
        + usage_charges
    )

    # Calculate tax using country/region
    tax_result = calculate_tax(
        amount=float(subtotal),
        country=country,
        region=region
    )

    tax_rate = Decimal(str(tax_result["tax_rate"]))
    tax = Decimal(str(tax_result["tax_amount"]))
    total = Decimal(str(tax_result["total"]))

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
        "total": total.quantize(Decimal("0.01")),
        "country": country.upper(),
        "region": region.upper() if region else None
    }