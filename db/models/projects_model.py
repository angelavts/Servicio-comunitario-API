from datetime import datetime
from db.session import Base
from db.enums import project_status_enum, ProjectStatusEnum
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    date_start = Column(DateTime(), default=datetime.now())
    date_end = Column(DateTime(), nullable=True)
    status = Column(project_status_enum, nullable=False, default=ProjectStatusEnum.Active)
    coordinator_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    career_id = Column(Integer(), ForeignKey('careers.id'), nullable=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())


    students = relationship('User', secondary='projects_students', back_populates='projects')

    def __str__(self):
        return self.name