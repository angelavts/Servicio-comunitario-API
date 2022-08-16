from datetime import datetime
from db.session import Base
from db.enums import Status
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint


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
    status = Column(String(20), nullable=False, default=Status.PENDING)
    student_id = Column(Integer(), nullable=False)
    project_id = Column(Integer(), nullable=False)
    tutor_id = Column(Integer(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.name