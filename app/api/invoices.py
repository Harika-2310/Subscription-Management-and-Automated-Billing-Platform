from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.crud.invoice import create_invoice

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post("/", response_model=InvoiceResponse)
def add_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    return create_invoice(db, invoice)