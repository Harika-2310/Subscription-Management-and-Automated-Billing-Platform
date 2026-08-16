from decimal import Decimal

from app.services.invoice_service import calculate_invoice


result = calculate_invoice(
    plan_fee=Decimal("1000"),
    proration_amount=Decimal("250"),
    usage_charges=Decimal("100"),
    tax_rate=Decimal("18")
)

print(result)