from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


def create_access_token(data: dict):
    """JWT（通行証）を発行する関数"""
    to_encode = data.copy()

    # 有効期限（exp）を設定
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    # ペイロード（データ）、シークレットキー、アルゴリズムを使って暗号化（署名）
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt
