from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.plan import PlanCreate, PlanUpdate, PlanResponse
from app.crud.plan import (
    create_plan,
    get_all_plans,
    update_plan,
    archive_plan
)

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.post("/", response_model=PlanResponse)
def add_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    return create_plan(db, plan)


@router.get("/", response_model=list[PlanResponse])
def list_plans(db: Session = Depends(get_db)):
    return get_all_plans(db)


@router.put("/{plan_id}", response_model=PlanResponse)
def edit_plan(plan_id: int, plan: PlanUpdate, db: Session = Depends(get_db)):
    updated = update_plan(db, plan_id, plan)

    if updated is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    return updated


@router.delete("/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    archived = archive_plan(db, plan_id)

    if archived is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    return {"message": "Plan archived successfully"}