import bcrypt
from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.user import UserCreate


def get_password_hash(password: str) -> str:
    """平文パスワードをハッシュ化する"""
    # bcryptはバイト列(bytes)を扱うため、encode()が必要
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    # DBには文字列(str)として保存するためdecode()
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードが正しいか検証する"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_user_by_email(db: Session, email: str):
    """メールアドレスからユーザーを検索する"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    """新しいユーザーをデータベースに登録する"""
    # 1. パスワードをハッシュ化する
    hashed_password = get_password_hash(user.password)

    # 2. 保存用のDBモデル（User）に変換する
    db_user = User(username=user.username, email=user.email, password_hash=hashed_password)

    # 3. DBに追加して保存（コミット）する
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # 保存されて自動採番されたIDなどを取得

    return db_user
