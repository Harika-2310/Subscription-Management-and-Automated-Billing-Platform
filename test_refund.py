from decimal import Decimal

from app.services.refund_service import calculate_refund


result = calculate_refund(
    plan_price=Decimal("1000"),
    days_used=10,
    total_cycle_days=30
)

print(result)