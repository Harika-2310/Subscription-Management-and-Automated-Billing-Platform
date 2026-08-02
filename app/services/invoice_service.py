from datetime import date

def generate_invoice(subscription):
    print(
        f"Invoice generated for Subscription {subscription.id} on {date.today()}"
    )