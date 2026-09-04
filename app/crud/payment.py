from sqlalchemy.orm import Session
from datetime import datetime

from app.models.payment import Payment
from app.models.invoice import Invoice
from app.models.subscription import Subscription

from app.services.payment_service import (
    process_payment,
    get_next_retry_time
)


# =========================================================
# MAKE PAYMENT
# =========================================================

def make_payment(
    db: Session,
    payment,
    success_rate: int = 80
):
    """
    Make a payment for an invoice.

    Used by app/api/payments.py
    """

    invoice = db.query(Invoice).filter(
        Invoice.id == payment.invoice_id
    ).first()

    if not invoice:
        return None

    result = process_payment(
        amount=payment.amount,
        success_rate=success_rate
    )

    now = datetime.utcnow()

    new_payment = Payment(
        invoice_id=payment.invoice_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=result["status"],
        retry_count=0,
        last_attempt_at=now,
        next_retry_at=(
            get_next_retry_time(1,now)
            if result["status"] == "failed"
            else None
        ),
        original_failure_at=(
    now
    if result["status"] == "failed"
    else None
),
        paid_at=(
            now
            if result["status"] == "paid"
            else None
        )
    )

    db.add(new_payment)

    # -----------------------------------------------------
    # Update invoice
    # -----------------------------------------------------

    if result["status"] == "paid":
        invoice.status = "paid"
    else:
        invoice.status = "failed"

    # -----------------------------------------------------
    # Find subscription
    # -----------------------------------------------------

    subscription = db.query(Subscription).filter(
        Subscription.id == invoice.subscription_id
    ).first()

    # -----------------------------------------------------
    # Update subscription
    # -----------------------------------------------------

    if subscription:

        if result["status"] == "paid":
            subscription.status = "active"

        else:
            subscription.status = "past_due"

    db.commit()
    db.refresh(new_payment)

    return new_payment


# =========================================================
# CREATE PAYMENT
# =========================================================

def create_payment(
    db: Session,
    invoice_id: int,
    amount: float,
    payment_method: str,
    success_rate: int = 80
):
    """
    Create a payment using individual payment details.
    """

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        return None

    result = process_payment(
        amount=amount,
        success_rate=success_rate
    )

    now = datetime.utcnow()

    payment = Payment(
    invoice_id=payment.invoice_id,
    amount=payment.amount,
    payment_method=payment.payment_method,
    status=result["status"],
    retry_count=0,
    last_attempt_at=now,

    next_retry_at=(
        get_next_retry_time(1, now)
        if result["status"] == "failed"
        else None
    ),

    original_failure_at=(
        now
        if result["status"] == "failed"
        else None
    ),

    paid_at=(
        now
        if result["status"] == "paid"
        else None
    )
)
    db.add(payment)

    if result["status"] == "paid":
        invoice.status = "paid"
    else:
        invoice.status = "failed"

    subscription = db.query(Subscription).filter(
        Subscription.id == invoice.subscription_id
    ).first()

    if subscription:

        if result["status"] == "paid":
            subscription.status = "active"
        else:
            subscription.status = "past_due"

    db.commit()
    db.refresh(payment)

    return payment


# =========================================================
# RETRY FAILED PAYMENT
# =========================================================

def retry_failed_payment(
    db: Session,
    payment_id: int,
    success_rate: int = 80
):
    """
    Retry a failed payment.

    Retry schedule:
        Retry 1 -> Day 1
        Retry 2 -> Day 3
        Retry 3 -> Day 7

    After 3 failed retries:
        Subscription -> cancelled
    """

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        return None

    # Only failed payments can be retried
    if payment.status != "failed":
        return payment

    # Maximum 3 retry attempts
    if payment.retry_count >= 3:
        return payment

    # -----------------------------------------------------
    # Process retry
    # -----------------------------------------------------

    result = process_payment(
        amount=payment.amount,
        success_rate=success_rate
    )

    now = datetime.utcnow()

    # Increase retry count
    payment.retry_count += 1
    payment.last_attempt_at = now

    # -----------------------------------------------------
    # Find invoice
    # -----------------------------------------------------

    invoice = db.query(Invoice).filter(
        Invoice.id == payment.invoice_id
    ).first()

    # -----------------------------------------------------
    # Find subscription
    # -----------------------------------------------------

    subscription = None

    if invoice:

        subscription = db.query(Subscription).filter(
            Subscription.id == invoice.subscription_id
        ).first()

    # =====================================================
    # PAYMENT SUCCESS
    # =====================================================

    if result["status"] == "paid":

        payment.status = "paid"
        payment.paid_at = now
        payment.next_retry_at = None

        if invoice:
            invoice.status = "paid"

        if subscription:
            subscription.status = "active"

    # =====================================================
    # PAYMENT FAILED
    # =====================================================

    else:

        payment.status = "failed"

        # -------------------------------------------------
        # All 3 retries exhausted
        # -------------------------------------------------

        if payment.retry_count >= 3:

            payment.next_retry_at = None

            if subscription:
                subscription.status = "cancelled"

        # -------------------------------------------------
        # Schedule next retry
        # -------------------------------------------------

        else:

            payment.next_retry_at = get_next_retry_time(
                payment.retry_count, payment.original_failure_at
            )

            if subscription:
                subscription.status = "past_due"

    db.commit()
    db.refresh(payment)

    return payment