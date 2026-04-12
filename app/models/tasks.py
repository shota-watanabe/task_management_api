from sqlalchemy import Column, BigInteger, String, Text, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey(
        "projects.id", ondelete="CASCADE"), nullable=False)
    # 担当者は未アサイン(NULL)を許容し、ユーザー削除時は担当者のみNULLにする(SET NULL)
    assigned_user_id = Column(BigInteger, ForeignKey(
        "users.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(128), nullable=False)
    status = Column(String(20), server_default="todo", nullable=False)
    start_date = Column(Date, nullable=True)
    expire_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey(
        "tasks.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)


class Label(Base):
    __tablename__ = "labels"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    color_code = Column(String(7), nullable=True)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)


class TaskLabel(Base):
    __tablename__ = "task_labels"

    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    label_id = Column(BigInteger, ForeignKey("labels.id", ondelete="CASCADE"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 複合ユニーク制約
    __table_args__ = (
        UniqueConstraint("task_id", "label_id", name="uq_task_label"),
    )
