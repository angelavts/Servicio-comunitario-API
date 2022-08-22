from datetime import datetime
from db.session import Base
from db.enums import role_enum, user_status_enum
from sqlalchemy import String, Boolean, Integer, Column, Text, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from db.models.institutions_model import Institution

class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    acronym = Column(String(100), nullable=False)
    id_institution = Column(Integer(), ForeignKey(Institution.id), nullable=False)
    institution = relationship(Institution)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.name