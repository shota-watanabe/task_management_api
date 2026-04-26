from fastapi import FastAPI

from app.routers import auth, project

app = FastAPI(title="チーム向けタスク管理API", version="1.0.0")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(project.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Hello World! FastAPIのDocker環境構築が成功しました！"}
