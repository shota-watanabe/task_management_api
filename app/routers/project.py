from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import project as crud_project
from app.database import get_db
from app.models.users import User
from app.routers.deps import get_current_user
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """新しいプロジェクトを作成する"""
    # crud側に、送られてきたデータと「ログイン中ユーザーのID」を渡す
    return crud_project.create_project(db=db, project=project, owner_id=current_user.id)


@router.get("", response_model=List[ProjectResponse])
def read_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """ログイン中のユーザーが作成したプロジェクト一覧を取得する"""
    return crud_project.get_projects_by_user(db=db, owner_id=current_user.id)
