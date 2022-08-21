from datetime import datetime
from db.session import Base
from db.enums import role_enum
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    identification = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(300), nullable=False)    
    id_career = Column(Integer(), nullable=True)
    total_hours = Column(Integer(), nullable=True)
    role = Column(role_enum, nullable=False)
    status = Column(String(20), nullable=True, default='Active')
    created_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.identification