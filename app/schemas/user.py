from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., max_length=50, description="ユーザー名")
    # EmailStr で形式チェックも含める
    email: EmailStr = Field(..., description="メールアドレス")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="パスワード")


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # SQLAlchemyのDBモデルをそのままJSONに変換
    model_config = ConfigDict(from_attributes=True)
