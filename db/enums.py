from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ENUM


status_enum = ('Pendiente','En progreso', 'Completada', 'Inactiva')
status_enum = ENUM(*status_enum, name='status_enum')

role_enum = ('Coordinador','Estudiante', 'Tutor')
role_enum = ENUM(*role_enum, name='role_enum')