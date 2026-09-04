from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_invoice_pdf(invoice):
    """
    Generate a PDF invoice and return it as bytes.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    normal_style = styles["Normal"]

    elements = []

    # Title
    elements.append(
        Paragraph("SUBSCRIPTION INVOICE", title_style)
    )

    elements.append(Spacer(1, 20))

    # Invoice information
    invoice_info = [
        ["Invoice Number", str(invoice.invoice_number)],
        ["Invoice ID", str(invoice.id)],
        ["Subscription ID", str(invoice.subscription_id)],
        ["Date", str(invoice.created_at)],
        ["Country", str(invoice.country)],
        ["Region", str(invoice.region or "-")],
        ["Status", str(invoice.status)]
    ]

    info_table = Table(
        invoice_info,
        colWidths=[150, 350]
    )

    info_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    elements.append(info_table)

    elements.append(Spacer(1, 20))

    # Amount details
    amount_data = [
        ["Description", "Amount"],
        ["Plan Fee", f"{invoice.plan_fee}"],
        ["Proration", f"{invoice.proration_amount}"],
        ["Usage Charges", f"{invoice.usage_charges}"],
        ["Subtotal", f"{invoice.subtotal}"],
        [
            f"Tax ({invoice.tax_rate}%)",
            f"{invoice.tax}"
        ],
        ["TOTAL", f"{invoice.total}"]
    ]

    amount_table = Table(
        amount_data,
        colWidths=[350, 150]
    )

    amount_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (1, -1), "RIGHT"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    elements.append(amount_table)

    elements.append(Spacer(1, 30))

    elements.append(
        Paragraph(
            "Thank you for your business.",
            normal_style
        )
    )

    document.build(elements)

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes