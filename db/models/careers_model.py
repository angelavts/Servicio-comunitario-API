from datetime import datetime
from db.session import Base
from db.enums import role_enum, user_status_enum
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

class Career(Base):
    __tablename__ = 'careers'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    faculty_id = Column(Integer(), ForeignKey('faculties.id'), nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.name