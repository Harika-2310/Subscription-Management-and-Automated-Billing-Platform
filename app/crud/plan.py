from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanUpdate


def create_plan(db: Session, plan: PlanCreate):
    db_plan = Plan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def get_all_plans(db: Session):
    return db.query(Plan).all()


def update_plan(db: Session, plan_id: int, plan: PlanUpdate):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not db_plan:
        return None

    for key, value in plan.model_dump().items():
        setattr(db_plan, key, value)

    db.commit()
    db.refresh(db_plan)
    return db_plan


def archive_plan(db: Session, plan_id: int):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not db_plan:
        return None

    db_plan.is_active = False
    db.commit()
    db.refresh(db_plan)

    return db_plan