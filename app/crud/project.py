from sqlalchemy.orm import Session

from app.models.projects import Project
from app.schemas.project import ProjectCreate


def create_project(db: Session, project: ProjectCreate, owner_id: int):
    """
    新しいプロジェクトをデータベースに登録する
    """
    # Pydanticのモデルを辞書（dict）に変換
    db_project = Project(**project.model_dump(), owner_id=owner_id)

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def get_projects_by_user(db: Session, owner_id: int):
    """
    特定のユーザーが作成したプロジェクト一覧を取得する
    """
    return db.query(Project).filter(Project.owner_id == owner_id).all()
