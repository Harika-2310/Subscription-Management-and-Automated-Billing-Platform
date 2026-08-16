from decimal import Decimal


def calculate_proration(
    old_price: Decimal,
    new_price: Decimal,
    days_remaining: int,
    total_cycle_days: int
):
    if total_cycle_days <= 0:
        raise ValueError("Total cycle days must be greater than zero")

    if days_remaining < 0:
        raise ValueError("Days remaining cannot be negative")

    if days_remaining > total_cycle_days:
        raise ValueError(
            "Days remaining cannot be greater than total cycle days"
        )

    old_unused_credit = (
        old_price / Decimal(total_cycle_days)
    ) * Decimal(days_remaining)

    new_remaining_cost = (
        new_price / Decimal(total_cycle_days)
    ) * Decimal(days_remaining)

    proration_amount = new_remaining_cost - old_unused_credit

    return {
        "old_unused_credit": old_unused_credit.quantize(Decimal("0.01")),
        "new_remaining_cost": new_remaining_cost.quantize(Decimal("0.01")),
        "proration_amount": proration_amount.quantize(Decimal("0.01"))
    }