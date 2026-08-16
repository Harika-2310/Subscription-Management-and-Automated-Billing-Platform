from decimal import Decimal

from app.services.proration import calculate_proration


result = calculate_proration(
    old_price=Decimal("500"),
    new_price=Decimal("1000"),
    days_remaining=15,
    total_cycle_days=30
)

print(result)