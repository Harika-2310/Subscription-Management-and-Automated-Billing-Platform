from pydantic import BaseModel
from datetime import datetime


class AuditLogCreate(BaseModel):
    action: str
    performed_by: str


class AuditLogResponse(BaseModel):
    id: int
    action: str
    performed_by: str
    created_at: datetime

    class Config:
        from_attributes = True