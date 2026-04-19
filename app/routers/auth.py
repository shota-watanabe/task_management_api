from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.crud import user as crud_user
from app.database import get_db
from app.models.users import User
from app.routers.deps import get_current_user
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):

    db_user = crud_user.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="このメールアドレスは既に登録されています。")

    return crud_user.create_user(db=db, user=user)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # ユーザーがデータベースに存在するか確認
    user = crud_user.get_user_by_email(db, email=form_data.username)

    # ユーザーが存在しない、またはパスワードが間違っている場合はエラーを返す
    if not user or not crud_user.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが間違っています",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 認証成功！ JWT（通行証）を発行する
    access_token = create_access_token(data={"sub": user.email})

    # 発行した通行証を返す
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Depends(get_current_user) を引数に入れるだけで、
    このAPIは「ログイン必須」になり、変数 current_user にログイン中のユーザー情報が自動で入る
    """
    return current_user
