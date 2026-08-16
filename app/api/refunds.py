from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.refund import RefundCreate, RefundResponse
from app.crud.refund import create_refund


router = APIRouter(
    prefix="/refunds",
    tags=["Refunds"]
)


@router.post(
    "/",
    response_model=RefundResponse
)
def add_refund(
    refund: RefundCreate,
    db: Session = Depends(get_db)
):

    result = create_refund(
        db=db,
        invoice_id=refund.invoice_id,
        refund_amount=refund.refund_amount,
        reason=refund.reason
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return result