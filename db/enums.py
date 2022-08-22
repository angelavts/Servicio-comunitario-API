from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ENUM


task_status_enum = ('Pendiente','En progreso', 'Completada', 'Inactiva')
task_status_enum = ENUM(*task_status_enum, name='task_status_enum')

role_enum = ('Coordinador','Estudiante', 'Tutor')
role_enum = ENUM(*role_enum, name='role_enum')


user_status_enum = ('Activo','Inactivo', 'Aprobado')
user_status_enum = ENUM(*user_status_enum, name='user_status_enum')