from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.subscription import Subscription
from app.models.payment import Payment
from app.models.plan import Plan


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):
    # Active subscriptions
    active_subscriptions = db.query(
        Subscription
    ).filter(
        Subscription.status == "active"
    ).all()

    # Calculate MRR
    mrr = 0

    for subscription in active_subscriptions:
        plan = db.query(Plan).filter(
            Plan.id == subscription.plan_id
        ).first()

        if plan:
            mrr += float(plan.price)

    # Failed payments
    failed_payments = db.query(
        Payment
    ).filter(
        Payment.status == "failed"
    ).count()

    # Cancelled subscriptions
    cancelled_subscriptions = db.query(
        Subscription
    ).filter(
        Subscription.status == "cancelled"
    ).count()

    total_subscriptions = db.query(
        Subscription
    ).count()

    # Churn rate
    if total_subscriptions > 0:
        churn_rate = (
            cancelled_subscriptions
            / total_subscriptions
        ) * 100
    else:
        churn_rate = 0

    return {
        "mrr": round(mrr, 2),
        "churn_rate": round(churn_rate, 2),
        "trial_conversion": 0,
        "failed_payments": failed_payments
    }
@router.get("/failed-payments")
def failed_payments(
    db: Session = Depends(get_db)
):
    payments = db.query(Payment).filter(
        Payment.status == "failed"
    ).order_by(
        Payment.id.desc()
    ).all()

    return payments