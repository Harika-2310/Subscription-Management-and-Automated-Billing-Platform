from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.audit_log import (
    AuditLogCreate,
    AuditLogResponse
)
from app.crud.audit_log import create_audit_log

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.post("/", response_model=AuditLogResponse)
def add_log(
    audit: AuditLogCreate,
    db: Session = Depends(get_db)
):
    return create_audit_log(db, audit)