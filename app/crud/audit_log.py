from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate


def create_audit_log(db: Session, audit: AuditLogCreate):

    log = AuditLog(
        action=audit.action,
        performed_by=audit.performed_by
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log