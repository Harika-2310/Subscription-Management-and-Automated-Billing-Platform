from sqlalchemy.orm import Session
from app.models.billing_cycle import BillingCycle
from app.schemas.billing_cycle import BillingCycleCreate


def create_billing_cycle(db: Session, billing: BillingCycleCreate):

    cycle = BillingCycle(
        subscription_id=billing.subscription_id,
        billing_date=billing.billing_date,
        next_billing_date=billing.next_billing_date,
        status="pending"
    )

    db.add(cycle)
    db.commit()
    db.refresh(cycle)

    return cycle