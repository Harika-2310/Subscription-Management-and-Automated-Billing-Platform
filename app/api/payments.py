from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.crud.payment import make_payment

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/", response_model=PaymentResponse)
def pay(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    return make_payment(db, payment)