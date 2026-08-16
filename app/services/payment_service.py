import random


def process_payment(
    amount: float,
    success_rate: int = 80
):
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