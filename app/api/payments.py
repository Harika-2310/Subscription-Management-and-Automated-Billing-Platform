from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.crud.payment import create_payment


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/process",
    response_model=PaymentResponse
)
def process_payment_api(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):

    result = create_payment(
        db=db,
        invoice_id=payment.invoice_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        success_rate=payment.success_rate
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return result