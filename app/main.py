from fastapi import FastAPI

app = FastAPI(title="社内リソース予約管理API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello World! FastAPIの環境構築が完了しました！"}
