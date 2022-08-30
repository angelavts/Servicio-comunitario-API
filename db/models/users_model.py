from datetime import datetime
from db.session import Base
from db.enums import role_enum, user_status_enum, UserStatusEnum
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    identification = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(300), nullable=False)    
    career_id = Column(Integer(), ForeignKey('careers.id'), nullable=True)
    total_hours = Column(Integer(), nullable=True)
    role = Column(role_enum, nullable=False)
    status = Column(user_status_enum, nullable=False, default=UserStatusEnum.Active)
    date_approval = Column(DateTime(), nullable=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())
    projects = relationship('Project', secondary='projects_students', back_populates='students')

    def __str__(self):
        return self.identification