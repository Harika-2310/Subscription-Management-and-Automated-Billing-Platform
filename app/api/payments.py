from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.crud.payment import make_payment
from app.crud.payment import create_payment
from app.crud.payment import retry_failed_payment

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/", response_model=PaymentResponse)
def pay(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    return make_payment(db, payment,success_rate=0)


@router.post("/retry/{payment_id}", response_model=PaymentResponse)
def retry_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = retry_failed_payment(
        db,
        payment_id,
        success_rate=0
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment