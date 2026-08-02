from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.subscription import Subscription,SubscriptionStatus
from app.models.plan import Plan
from app.schemas.subscription import SubscriptionCreate


def create_subscription(db: Session, subscription: SubscriptionCreate):

    plan = db.query(Plan).filter(
        Plan.id == subscription.plan_id
    ).first()

    if not plan:
        return None

    trial_end = datetime.utcnow() + timedelta(days=plan.trial_days)

    db_subscription = Subscription(
        user_id=subscription.user_id,
        plan_id=subscription.plan_id,
        status=SubscriptionStatus.trial,
        start_date=datetime.utcnow(),
        trial_end=trial_end
    )

    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)

    return db_subscription


VALID_TRANSITIONS = {
    SubscriptionStatus.trial: [
        SubscriptionStatus.active,
        SubscriptionStatus.cancelled
    ],
    SubscriptionStatus.active: [
        SubscriptionStatus.past_due
    ],
    SubscriptionStatus.past_due: [
        SubscriptionStatus.cancelled
    ],
    SubscriptionStatus.cancelled: []
}


def change_subscription_status(db: Session, subscription_id: int, new_status: str):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None, "Subscription not found"

    current_status = subscription.status
    target_status = SubscriptionStatus(new_status)
    if target_status not in VALID_TRANSITIONS[current_status]:
        return None, f"Invalid transition from {current_status.value} to {new_status}"

    subscription.status = target_status
    subscription.status = SubscriptionStatus(new_status)

    db.commit()
    db.refresh(subscription)

    return subscription, None


# ----------------------------
# ADD THIS FUNCTION BELOW
# ----------------------------

def change_plan(db: Session, subscription_id: int, new_plan_id: int):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    plan = db.query(Plan).filter(
        Plan.id == new_plan_id
    ).first()

    if not plan:
        return False

    subscription.plan_id = new_plan_id

    db.commit()
    db.refresh(subscription)

    return subscription
def pause_subscription(db: Session, subscription_id: int):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    subscription.paused = True

    db.commit()
    db.refresh(subscription)

    return subscription
def resume_subscription(db: Session, subscription_id: int):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    subscription.paused = False

    db.commit()
    db.refresh(subscription)

    return subscription
def cancel_subscription(db: Session, subscription_id: int, immediate: bool):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    if immediate:
        subscription.status = SubscriptionStatus.cancelled
        subscription.end_date = datetime.utcnow()
    else:
        subscription.cancel_at_period_end = True

    db.commit()
    db.refresh(subscription)

    return subscription