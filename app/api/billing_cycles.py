from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.billing_cycle import (
    BillingCycleCreate,
    BillingCycleResponse
)
from app.crud.billing_cycle import create_billing_cycle

router = APIRouter(
    prefix="/billing-cycles",
    tags=["Billing Cycles"]
)


@router.post("/", response_model=BillingCycleResponse)
def add_cycle(
    billing: BillingCycleCreate,
    db: Session = Depends(get_db)
):
    return create_billing_cycle(db, billing)