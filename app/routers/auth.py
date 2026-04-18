from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as crud_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):

    db_user = crud_user.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="このメールアドレスは既に登録されています。"
        )

    return crud_user.create_user(db=db, user=user)
