from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SubscriptionCreate(BaseModel):
    user_id: int
    plan_id: int


class ChangePlan(BaseModel):
    plan_id: int


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    status: str
    start_date: datetime
    trial_end: Optional[datetime]
    end_date: Optional[datetime]

    class Config:
        from_attributes = True