from datetime import datetime
from db.session import Base
from db.enums import role_enum, user_status_enum
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from db.models.faculties_model import Faculty 

class Career(Base):
    __tablename__ = 'careers'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    id_faculty = Column(Integer(), ForeignKey(Faculty.id), nullable=False)
    faculty = relationship(Faculty)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.name