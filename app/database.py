import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "")

# DBとの接続エンジンを作成 (echo=True にすると、発行されたSQLがターミナルに表示されてデバッグしやすい)
engine = create_engine(DATABASE_URL, echo=True)

# データベースにアクセスするための「セッション」を作成する工場
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 各テーブル定義（Model）の親となるベースクラス
Base = declarative_base()

# FastAPIの依存関係注入（DI）で使う、DBセッション取得関数
# APIが呼ばれるたびにDB接続を開き、処理が終わったら必ず閉じる
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
