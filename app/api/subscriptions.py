from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
    ChangePlan
)

from app.crud.subscription import (
    create_subscription,
    change_subscription_status,
    change_plan,
    pause_subscription,
    resume_subscription,
    cancel_subscription
)

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


# -----------------------------
# Create Subscription
# -----------------------------
@router.post("/", response_model=SubscriptionResponse)
def add_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db)
):
    result = create_subscription(db, subscription)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    return result


# -----------------------------
# Update Subscription Status
# -----------------------------
@router.put("/{subscription_id}/status")
def update_status(
    subscription_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):
    subscription, error = change_subscription_status(
        db,
        subscription_id,
        new_status
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "Subscription updated successfully",
        "status": subscription.status
    }


# -----------------------------
# Change Plan
# -----------------------------
@router.put("/{subscription_id}/change-plan")
def update_plan(
    subscription_id: int,
    request: ChangePlan,
    db: Session = Depends(get_db)
):
    result = change_plan(
        db,
        subscription_id,
        request.plan_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    if result is False:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    return {
        "message": "Plan changed successfully",
        "subscription_id": result["subscription"].id,
        "new_plan_id": result["subscription"].plan_id,
        "proration": result["proration"]
    }
@router.put("/{subscription_id}/pause")
def pause(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    subscription = pause_subscription(
        db,
        subscription_id
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    return {
        "message": "Subscription paused successfully"
    }
# -----------------------------
# Resume Subscription
# -----------------------------
@router.put("/{subscription_id}/resume")
def resume(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    subscription = resume_subscription(
        db,
        subscription_id
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    return {
        "message": "Subscription resumed successfully"
    }
@router.put("/{subscription_id}/cancel")
def cancel(
    subscription_id: int,
    immediate: bool,
    db: Session = Depends(get_db)
):

    subscription = cancel_subscription(
        db,
        subscription_id,
        immediate
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    if immediate:
        return {
            "message": "Subscription cancelled immediately"
        }

    return {
        "message": "Subscription will cancel at period end"
    }