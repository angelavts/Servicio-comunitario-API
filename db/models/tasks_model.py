from datetime import datetime
from db.session import Base
from db.enums import task_status_enum, TaskStatusEnum
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint, ForeignKey
from db.models.users_model import User

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        UniqueConstraint('student_id', 'project_id', 'name'),
    )
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300), nullable=True)
    cost = Column(Integer(), nullable=False)
    date_start = Column(DateTime(), default=datetime.now())
    date_end = Column(DateTime(), nullable=True)
    status = Column(task_status_enum, nullable=False, default=TaskStatusEnum.Pending)
    student_id = Column(Integer(), ForeignKey(User.id), nullable=False)
    tutor_id = Column(Integer(), ForeignKey(User.id), nullable=True)
    project_id = Column(Integer(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.name