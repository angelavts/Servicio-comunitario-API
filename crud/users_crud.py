from db import db_models as models
from db.enums import RoleEnum, UserStatusEnum
from schemas.users_schema import User
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from fastapi import status, HTTPException
from typing import List
from core import utils
from core.messages import messages
from datetime import datetime
from sqlalchemy import any_, exists, func, case
from itertools import groupby


# ------------------------------------------ POST ------------------------------------

def create_user(user: User, role: str, db: Session):
    """
    Crea un usuario 
    """
    db_user = db.query(models.User).filter(models.User.identification == user.identification).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail=messages['user_exists'])
    new_user = build_new_user(user, role, db) 
    try:
        db.add(new_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return new_user
    
def create_users_from_list(users: List[User], role: str, db: Session):
    """
    Crear usuarios a partir de una lista
    """
    response = {}
    successful = []
    failed = []
    for user in users:
        # se debe verificar que el formato de cédula es correcto
        if utils.is_valid_identication(user.identification):
            new_user = build_new_user(user, role, db)
            try:
                db.add(new_user)
                db.commit()
                successful.append(user)
            except Exception as e:
                db.rollback()
                failed.append({'User': user, 'detail': str(e)})
        else:
            failed.append({'User': user, 'detail': messages['invalid_id_format']})

    response['successful'] = successful
    response['failed'] = failed        
    return response

# ------------------------------------------ UPDATE ------------------------------------

def update_user(user: User, identification: str, db: Session):
    """
    Crea un usuario 
    """
    db_user = db.query(models.User).filter(models.User.identification == user.identification).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])
    # revisar si existe la carrera 
    db_career = db.query(models.Career).filter(models.Career.name == user.career).first()
    # cambiar datos del usuario
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.career_id = db_career.id
    try:
        db.add(db_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_user

def update_student_status(identification: str, status: str, db: Session):
    """
    Actualiza el status de un estudiante
    """
    db_user = db.query(models.User).filter(models.User.identification == identification).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])
    # cambiar el estatus
    db_user.status = status
    # si el estudiante es aprobado, se coloca su fecha de finalización
    if status == UserStatusEnum.Approved:
        date_approval = datetime.now()
    try:
        # actualizar base de datos
        db.add(db_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_user

# ------------------------------------------ GET ------------------------------------


def get_user_by_identification(identification: str, db: Session):
    """
    Obtiene un usuario a partir de la cédula
    """
    db_user = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    models.User.total_hours, 
                    models.User.status,
                    models.User.date_approval,   
                    models.User.career_id,                      
                    models.Career.name.label('career_name'))
                .outerjoin(models.Career, models.Career.id == models.User.career_id)
                .filter(models.User.identification == identification).first())
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])
    return db_user



def get_students(db: Session, status: str=None):
    """
    Obtener una lista de estudiantes con los siguientes campos
    Cédula, nombre, apellido, horas, estatus, proyecto, fecha de aprobación
    """
    filters = [models.User.role == RoleEnum.Student]
    if status is not None:
        filters = [models.User.status == status]

    projects_alias = aliased(models.Project, name='project')
    career_alias = aliased(models.Career, name='career')
    db_students = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    models.User.total_hours, 
                    models.User.status,
                    models.User.date_approval,
                    career_alias, 
                    projects_alias)
                .filter(*filters)
                .outerjoin(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                .filter(models.ProjectStudent.active)
                .outerjoin(projects_alias, projects_alias.id == models.ProjectStudent.project_id)   
                .outerjoin(career_alias, career_alias.id == models.User.career_id)                
                .all())
    return db_students

def get_approved_students(db: Session):
    """
    Obtener una lista de estudiantes con los siguientes campos
    Cédula, nombre, apellido, horas, estatus, proyecto, fecha de aprobación
    """
    filters = [models.User.role == RoleEnum.Student, models.User.status == UserStatusEnum.Approved]

    projects_alias = aliased(models.Project, name='project')
    career_alias = aliased(models.Career, name='career')
    db_students = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    career_alias.name.label('career'), 
                    projects_alias.name.label('project'),
                    models.User.total_hours, 
                    models.User.date_approval)
                .filter(*filters)
                .outerjoin(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                .filter(models.ProjectStudent.active)
                .outerjoin(projects_alias, projects_alias.id == models.ProjectStudent.project_id)   
                .outerjoin(career_alias, career_alias.id == models.User.career_id)                
                .all())
    return db_students

def get_students_with_project(db: Session):
    """
    Obtener una lista de estudiantes con los siguientes campos
    Cédula, nombre, apellido, horas, estatus, proyecto, fecha de aprobación
    """
    filters = [models.User.role == RoleEnum.Student, models.User.status == UserStatusEnum.Active]

    projects_alias = aliased(models.Project, name='project')
    career_alias = aliased(models.Career, name='career')
    db_students = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    career_alias.name.label('career'), 
                    projects_alias.name.label('project'),
                    models.User.total_hours)
                .filter(*filters)
                .outerjoin(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                .filter(models.ProjectStudent.active)
                .outerjoin(projects_alias, projects_alias.id == models.ProjectStudent.project_id)   
                .outerjoin(career_alias, career_alias.id == models.User.career_id)                
                .all())
    return db_students


def get_students_by_status(db: Session, status: str):
    """
    Obtener una lista de estudiantes activos o inactivos
    """
    filters = [models.User.role == RoleEnum.Student, models.User.status == status]
    career_alias = aliased(models.Career, name='career')
    db_students = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    career_alias.name.label('career'),
                    models.User.total_hours
                    )
                .filter(*filters)
                .outerjoin(career_alias, career_alias.id == models.User.career_id)                
                .all())
    return db_students

def get_students_without_project(db: Session):
    """
    Obtener una lista de estudiantes que no tienen proyecto activo
    es decir, que no existen en una relación ProjectStudent o que
    todas sus relaciones tienen active en falso 
    """
    filters = [models.User.role == RoleEnum.Student, models.User.status == UserStatusEnum.Active]
    career_alias = aliased(models.Career, name='career')
    db_user = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,                      
                    career_alias.name.label('career'), 
                    models.User.total_hours,
                    func.count(models.ProjectStudent.active)
                )
                .filter(*filters)
                .outerjoin(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                .group_by(career_alias, models.User.id)
                .having(func.count(1).filter(models.ProjectStudent.active) == 0)
                .outerjoin(career_alias, career_alias.id == models.User.career_id)
                ).all()            
    return db_user


def get_users_by_role(role: str, db: Session):
    """
    Obtiene una lista de usuarios según el rol indicado
    """
    db_users = (db.query(models.User.id,
                         models.User.identification, 
                         models.User.fullname,
                         models.User.total_hours, 
                         models.User.status, 
                         models.User.role,
                         models.User.career_id,                      
                        models.Career.name.label('career_name'))
                    .outerjoin(models.Career, models.Career.id == models.User.career_id)
                .filter(models.User.role == role)               
                .all())
    return db_users

def get_tutors(db: Session):
    """
    Obtiene una lista de usuarios según el rol indicado
    """
    career_alias = aliased(models.Career, name='career')
    db_users = (db.query(models.User.id,
                         models.User.identification, 
                         models.User.first_name, 
                         models.User.last_name,                     
                         career_alias)
                    .outerjoin(career_alias, career_alias.id == models.User.career_id)
                .filter(models.User.role == RoleEnum.Tutor)               
                .all())
    return db_users



def get_project_info_by_student(identification: str, db: Session):
    """5
        Busca información del proyecto donde se encuentra inscrito un estudiante    
    """
    coordinator = aliased(models.User, name='coordinator')
    project_info = (db.query(
                    models.Project.id,
                    models.Project.name,
                    models.Project.description, 
                    models.Project.date_start, 
                    coordinator.fullname.label('coordinator'))                
                .join(models.ProjectStudent, models.Project.id == models.ProjectStudent.project_id)
                .join(models.User, models.User.id == models.ProjectStudent.student_id)
                .filter(models.User.identification == identification)
                .filter(models.ProjectStudent.active)
                .join(coordinator, coordinator.id == models.Project.coordinator_id)
                .first())    
    return project_info

# ------------------------------------------ TOOLS ------------------------------------

def build_new_user(user: User, role: str, db: Session):
    # revisar si existe la carrera 
    db_career = db.query(models.Career).filter(models.Career.name == user.career).first()

    new_user = models.User(
        identification=user.identification,
        first_name=user.first_name,
        last_name=user.last_name,            
        role = role,
        career_id = db_career.id
    )  
    return new_user



