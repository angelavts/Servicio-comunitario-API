from datetime import datetime
from db.session import Base
from db.enums import role_enum, user_status_enum
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from db.models.careers_model import Career

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    identification = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(300), nullable=False)    
    id_career = Column(Integer(), ForeignKey(Career.id), nullable=True)
    career = relationship(Career)
    total_hours = Column(Integer(), nullable=True)
    role = Column(role_enum, nullable=False)
    status = Column(user_status_enum, nullable=False, default='Activo')
    created_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.identification