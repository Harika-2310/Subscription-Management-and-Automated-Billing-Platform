from datetime import timedelta


def calculate_next_billing(subscription, plan):
    """
    Calculate the next billing date based on the plan.
    """

    if plan.billing_interval == "monthly":
        return subscription.start_date + timedelta(days=30)

    elif plan.billing_interval == "annual":
        return subscription.start_date + timedelta(days=365)

    return None