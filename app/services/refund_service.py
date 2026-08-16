from decimal import Decimal


def calculate_refund(
    plan_price: Decimal,
    days_used: int,
    total_cycle_days: int
):
    if total_cycle_days <= 0:
        raise ValueError("Total cycle days must be greater than zero")

    if days_used < 0 or days_used > total_cycle_days:
        raise ValueError("Invalid days used")

    unused_days = total_cycle_days - days_used

    refund = (
        plan_price
        / Decimal(total_cycle_days)
    ) * Decimal(unused_days)

    return {
        "plan_price": plan_price.quantize(Decimal("0.01")),
        "days_used": days_used,
        "unused_days": unused_days,
        "refund_amount": refund.quantize(Decimal("0.01"))
    }