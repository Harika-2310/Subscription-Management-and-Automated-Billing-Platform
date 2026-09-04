from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from sqlalchemy.orm import Session
from app.services.pdf_service import generate_invoice_pdf
from app.models.invoice import Invoice

from app.database.database import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.crud.invoice import (
    create_invoice,
    get_tax_report
)


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


# =========================================================
# TAX REPORT
# =========================================================

@router.get("/tax-report")
def tax_report(
    db: Session = Depends(get_db)
):
    return get_tax_report(db)


# =========================================================
# CREATE INVOICE
# =========================================================
@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    pdf_bytes = generate_invoice_pdf(invoice)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f"attachment; filename={invoice.invoice_number}.pdf"
            )
        }
    )
@router.post("/", response_model=InvoiceResponse)
def add_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):

    result = create_invoice(
        db=db,
        subscription_id=invoice.subscription_id,
        usage_charges=invoice.usage_charges,
        country=invoice.country,
        region=invoice.region
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription or plan not found"
        )

    return result