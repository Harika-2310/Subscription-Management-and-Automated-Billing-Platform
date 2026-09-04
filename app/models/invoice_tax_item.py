from sqlalchemy import Column, Integer, Numeric, String, ForeignKey

from app.database.base import Base


class InvoiceTaxItem(Base):
    __tablename__ = "invoice_tax_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    country = Column(
        String(10),
        nullable=False
    )

    region = Column(
        String(50),
        nullable=True
    )

    tax_rate = Column(
        Numeric(5, 2),
        nullable=False
    )

    tax_amount = Column(
        Numeric(10, 2),
        nullable=False
    )