from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.subscription import Subscription, SubscriptionStatus
from app.models.plan import Plan
from app.models.invoice import Invoice
from app.models.refund import Refund

from app.schemas.subscription import SubscriptionCreate

from app.services.proration import calculate_proration
from app.services.refund_service import calculate_refund


# ============================================================
# CREATE SUBSCRIPTION
# ============================================================

def create_subscription(
    db: Session,
    subscription: SubscriptionCreate
):

    plan = db.query(Plan).filter(
        Plan.id == subscription.plan_id
    ).first()

    if not plan:
        return None

    trial_end = (
        datetime.utcnow()
        + timedelta(days=plan.trial_days)
    )

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


# ============================================================
# SUBSCRIPTION STATUS TRANSITIONS
# ============================================================

VALID_TRANSITIONS = {
    "trial": ["active", "cancelled"],
    "active": ["past_due"],
    "past_due": ["cancelled"],
    "cancelled": []
}


def change_subscription_status(
    db: Session,
    subscription_id: int,
    new_status: str
):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None, "Subscription not found"

    current_status = subscription.status

    if current_status not in VALID_TRANSITIONS:
        return None, f"Unknown subscription status: {current_status}"

    if new_status not in VALID_TRANSITIONS[current_status]:
        return None, (
            f"Invalid transition from "
            f"{current_status} to {new_status}"
        )

    subscription.status = new_status

    db.commit()
    db.refresh(subscription)

    return subscription, None


# ============================================================
# CHANGE PLAN + PRORATION
# ============================================================

def change_plan(
    db: Session,
    subscription_id: int,
    new_plan_id: int
):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    old_plan = db.query(Plan).filter(
        Plan.id == subscription.plan_id
    ).first()

    if not old_plan:
        return None

    new_plan = db.query(Plan).filter(
        Plan.id == new_plan_id
    ).first()

    if not new_plan:
        return False

    # Assume a 30-day billing cycle
    total_cycle_days = 30

    if subscription.start_date:
        days_used = (
            datetime.utcnow() - subscription.start_date
        ).days
    else:
        days_used = 0

    days_used = min(
        max(days_used, 0),
        total_cycle_days
    )

    days_remaining = (
        total_cycle_days - days_used
    )

    proration = calculate_proration(
        old_price=Decimal(str(old_plan.price)),
        new_price=Decimal(str(new_plan.price)),
        days_remaining=days_remaining,
        total_cycle_days=total_cycle_days
    )

    # Change plan
    subscription.plan_id = new_plan_id

    db.commit()
    db.refresh(subscription)

    return {
        "subscription": subscription,
        "proration": proration
    }


# ============================================================
# PAUSE SUBSCRIPTION
# ============================================================

def pause_subscription(
    db: Session,
    subscription_id: int
):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    subscription.paused = True

    db.commit()
    db.refresh(subscription)

    return subscription


# ============================================================
# RESUME SUBSCRIPTION
# ============================================================

def resume_subscription(
    db: Session,
    subscription_id: int
):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    subscription.paused = False

    db.commit()
    db.refresh(subscription)

    return subscription


# ============================================================
# CANCEL SUBSCRIPTION + AUTOMATIC REFUND
# ============================================================

def cancel_subscription(
    db: Session,
    subscription_id: int,
    immediate: bool
):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        return None

    # --------------------------------------------------------
    # IMMEDIATE CANCELLATION
    # --------------------------------------------------------

    if immediate:

        # Find current plan
        plan = db.query(Plan).filter(
            Plan.id == subscription.plan_id
        ).first()

        if plan:

            # Calculate used days
            if subscription.start_date:

                days_used = (
                    datetime.utcnow()
                    - subscription.start_date
                ).days

            else:
                days_used = 0

            # Monthly billing cycle
            total_cycle_days = 30

            # Keep value between 0 and 30
            days_used = min(
                max(days_used, 0),
                total_cycle_days
            )

            # Calculate unused-period refund
            refund_data = calculate_refund(
                plan_price=Decimal(
                    str(plan.price)
                ),
                days_used=days_used,
                total_cycle_days=total_cycle_days
            )

            # Find latest invoice
            invoice = db.query(Invoice).filter(
                Invoice.subscription_id == subscription_id
            ).order_by(
                Invoice.id.desc()
            ).first()

            # Create refund
            if (
                invoice
                and refund_data["refund_amount"] > 0
            ):

                refund = Refund(
                    invoice_id=invoice.id,
                    amount=refund_data["refund_amount"],
                    reason=(
                        "Subscription cancelled "
                        "with unused period"
                    ),
                    status="processed"
                )

                db.add(refund)

                # Update invoice
                invoice.status = "refunded"

        # Cancel subscription
        subscription.status = SubscriptionStatus.cancelled

        subscription.end_date = datetime.utcnow()

    # --------------------------------------------------------
    # END-OF-CYCLE CANCELLATION
    # --------------------------------------------------------

    else:

        subscription.cancel_at_period_end = True

    db.commit()
    db.refresh(subscription)

    return subscription