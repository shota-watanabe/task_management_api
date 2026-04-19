import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import user as crud_user
from app.database import get_db
from app.models.users import User

# Swagger UIに「Authorize」ボタンを作り、ログインAPIのURLを指定する
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    リクエストのヘッダーにあるJWT（通行証）を解読し、
    現在ログインしているユーザーのDBモデルを返す
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報が無効です。再度ログインしてください。",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # JWTを秘密鍵で解読（デコード）する
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except jwt.PyJWTError:  # 偽造されたトークンや、期限切れのトークンの場合
        raise credentials_exception

    user = crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user
