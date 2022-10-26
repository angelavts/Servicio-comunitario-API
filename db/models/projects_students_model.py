from datetime import datetime
from db.session import Base
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint, ForeignKey

class ProjectStudent(Base):
    __tablename__ = 'projects_students'
    __table_args__ = (
        UniqueConstraint('student_id', 'project_id'),
    )
    id = Column(Integer(), primary_key=True)
    active = Column(Boolean, nullable=False, default=True)
    project_id = Column(Integer(), ForeignKey('projects.id'), nullable=False)
    student_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.id