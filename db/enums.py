from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum


# Task status enum
class TaskStatusEnum(str, Enum):
    Pending = 'Pendiente'
    InProgress = 'En progreso'
    Completed = 'Completada'
    Inactive = 'Comunidad'

task_status_enum = ('Pendiente','En progreso', 'Completada', 'Inactiva')
task_status_enum = ENUM(*task_status_enum, name='task_status_enum')



# Role enum
role_enum = ('Coordinador','Estudiante', 'Tutor', 'Comunidad')
role_enum = ENUM(*role_enum, name='role_enum')

class RoleEnum(str, Enum):
    Coordinator = 'Coordinador'
    Student = 'Estudiante'
    Tutor = 'Tutor'
    Community = 'Comunidad'

# User status enum
class UserStatusEnum(str, Enum):
    Active = 'Activo'
    Inactive = 'Inactivo'
    Approved = 'Aprobado'

user_status_enum = ('Activo', 'Inactivo', 'Aprobado')
user_status_enum = ENUM(*user_status_enum, name='user_status_enum')

# Project status enum
project_status_enum = ('Activo','Inactivo')
project_status_enum = ENUM(*project_status_enum, name='project_status_enum')

class ProjectStatusEnum(str, Enum):
    Active = 'Activo'
    Inactive = 'Inactivo'



