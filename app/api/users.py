from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse,UserLogin, Token
from app.crud.user import create_user,login_user
from app.dependencies import get_current_user
from app.models.user import User
router = APIRouter(prefix="/users", tags=["Users"])
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token = login_user(db, form_data.username, form_data.password)

    if token is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return token
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user