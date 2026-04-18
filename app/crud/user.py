from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.users import User
from app.schemas.user import UserCreate

# パスワードハッシュ化の設定（bcryptアルゴリズムを使用）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """平文パスワードをハッシュ化する関数"""
    return pwd_context.hash(password)


def get_user_by_email(db: Session, email: str):
    """メールアドレスからユーザーを検索する（登録済みのチェックに使用）"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    """新しいユーザーをデータベースに登録する"""
    # 1. パスワードをハッシュ化する
    hashed_password = get_password_hash(user.password)

    # 2. 保存用のDBモデル（User）に変換する
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    # 3. DBに追加して保存（コミット）する
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # 保存されて自動採番されたIDなどを取得

    return db_user
