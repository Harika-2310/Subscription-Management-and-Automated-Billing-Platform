import random
from datetime import datetime, timedelta


# =========================================================
# MOCK PAYMENT PROCESSING
# =========================================================

def process_payment(
    amount: float,
    success_rate: int = 80
):
    """
    Simulate a payment.

    success_rate:
        0   = always fail
        100 = always succeed
        80  = 80% chance of success
    """

    if amount <= 0:
        return {
            "status": "failed",
            "message": "Invalid payment amount"
        }

    if not 0 <= success_rate <= 100:
        return {
            "status": "failed",
            "message": "Success rate must be between 0 and 100"
        }

    random_number = random.randint(1, 100)

    if random_number <= success_rate:
        return {
            "status": "paid",
            "message": "Payment successful"
        }

    return {
        "status": "failed",
        "message": "Payment failed"
    }


# =========================================================
# RETRY SCHEDULE
# =========================================================

RETRY_SCHEDULE = {
    1: 1,   # Retry 1 -> Day 1
    2: 3,   # Retry 2 -> Day 3
    3: 7    # Retry 3 -> Day 7
}


def get_next_retry_time(
    retry_count: int,
    original_failure_time: datetime = None
):
    """
    Calculate the next retry time.

    Retry 1 -> Day 1
    Retry 2 -> Day 3
    Retry 3 -> Day 7

    The schedule is calculated from the original
    payment failure time.
    """

    if retry_count not in RETRY_SCHEDULE:
        return None

    if original_failure_time is None:
        original_failure_time = datetime.utcnow()

    days = RETRY_SCHEDULE[retry_count]

    return original_failure_time + timedelta(days=days)