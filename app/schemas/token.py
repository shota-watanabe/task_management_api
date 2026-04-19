from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # JWTの中に埋め込むデータ
    email: str | None = None
