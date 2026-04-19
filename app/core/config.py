from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # .envファイルから自動で読み込まれる
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# アプリ全体で使い回せるようにインスタンス化
settings = Settings()
