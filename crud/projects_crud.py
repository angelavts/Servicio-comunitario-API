from db import db_models as models
from schemas.projects_schema import Project
from schemas.users_schema import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List
from core.messages import messages
from datetime import datetime



# --------------------------------------------- TOOLS ------------------------------------------------------------
def get_user_from_identification(identification: str, error_message: str, db: Session):
    # buscar el id del coordinador 
    db_user =  db.query(models.User).filter(models.User.identification == identification).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail=messages[error_message])
    
    return db_user

def get_career_from_name(name: str, error_message: str, db: Session):
    # buscar el id de la carrera 
    db_user =  db.query(models.Career).filter(models.Career.name == name).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail=messages[error_message])
    
    return db_user


# --------------------------------------------- POST ------------------------------------------------------------

def create(project: Project, db: Session):
    """
    Crea un proyecto 
    """

    # buscar el id del coordinador
    coordinator = get_user_from_identification(project.coordinator_identification, 'coordinator_not_exists', db)

    # buscar el id de la carrera
    career = get_career_from_name(project.career, 'career_not_exists', db)

    # Validacion de proyectos duplicados
    db_task = (
        db.query(models.Project).filter(models.Project.name == project.name).first()
    )
    if db_task is not None:
        raise HTTPException(status_code=400, detail=messages['project_exists'])


    new_project = models.Project(
        name=project.name,
        description=project.description,
        date_start=project.date_start,
        coordinator_id = coordinator.id,
        career_id = career.id,
    ) 

    try:
        db.add(new_project)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return new_project


# --------------------------------------------- UPDATE ------------------------------------------------------------
def update_project_status(project_id: int, status: str, db: Session):
    """
    Actualizar el status de un proyecto 
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=400, detail=messages['project_not_exists'])

    # cambiar status del proyecto
    project.status = status

    # ultima actualizacion
    project.updated_at = datetime.now()
    
    try:
        db.add(project)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return project

def update_project_date_end(project_id: int, date: datetime, db: Session):
    """
    Actualizar el status de un proyecto 
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=400, detail=messages['project_not_exists'])

    # finalizacion del proyecto
    project.date_end = date

    # ultima actualizacion
    project.updated_at = datetime.now()
    
    try:
        db.add(project)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return project


# --------------------------------------------- GET ------------------------------------------------------------
def get_projects_by_status(status: str, db: Session):
    """
    Obtiene una lista de proyectos por estatus
    """
    projects = (db.query(models.Project.id,
                         models.Project.name, 
                         models.Project.date_start, 
                         models.Project.date_end,
                         models.User.first_name.label('Coordinator name'), 
                         models.User.last_name.label('Coordinator last name'), 
                         models.Career.name.label('Career name'))
                         .join(models.User, models.User.id == models.Project.coordinator_id)
                         .join(models.Career, models.Career.id == models.Project.career_id)
                         .filter(models.Project.status == status)               
                ).all()
    return projects

def get_projects_by_coordinator_status(project: Project, status: str, db: Session):
    """
    Obtiene una lista de proyectos de un coordinador especifico por status
    """
    # buscar el id del coordinador
    coordinator = get_user_from_identification(project.coordinator_identification, 'coordinator_not_exists', db)

    projects = (db.query(models.Project.id,
                         models.Project.name, 
                         models.Project.date_start, 
                         models.Project.date_end,
                         models.User.first_name.label('Coordinator name'), 
                         models.User.last_name.label('Coordinator last name'), 
                         models.Career.name.label('Career name'))
                         .join(models.User, models.User.id == models.Project.coordinator_id)
                         .join(models.Career, models.Career.id == models.Project.career_id)
                         .filter(models.Project.coordinator_id == coordinator.id and models.Project.status == status)               
                ).all()
    return projects

def get_projects_by_career_status(project: Project, status: str, db: Session):
    """
    Obtiene una lista de proyectos de una carrera especifica por status
    """
    # buscar el id de la carrera
    career = get_career_from_name(project.career, 'career_not_exists', db)

    projects = (db.query(models.Project.id,
                         models.Project.name, 
                         models.Project.date_start, 
                         models.Project.date_end,
                         models.User.first_name.label('Coordinator name'), 
                         models.User.last_name.label('Coordinator last name'), 
                         models.Career.name.label('Career name'))
                         .join(models.User, models.User.id == models.Project.coordinator_id)
                         .join(models.Career, models.Career.id == models.Project.career_id)
                         .filter(models.Project.career_id == career.id and models.Project.status == status)               
                ).all()
    return projects

def get_project(project_id: int, db: Session):
    """
    Obtiene un proyecto
    """
    projects = (db.query(models.Project.id,
                         models.Project.name, 
                         models.Project.description,
                         models.Project.date_start, 
                         models.Project.date_end,
                         models.Project.status,
                         models.User.id.label('coordinator_id'), 
                         models.User.identification.label('coordinator_identification'), 
                         models.User.first_name.label('coordinator_first_name'), 
                         models.User.last_name.label('coordinator_last_name'), 
                         models.Career.name.label('career_name'))
                         .filter(models.Project.id == project_id)    
                         .join(models.User, models.User.id == models.Project.coordinator_id)
                         .join(models.Career, models.Career.id == models.Project.career_id)
                                    
                ).first()
    return projects

def get_active_project_by_student_id(student_id: int, db: Session):
    """
    Obtiene información de un proyecto a partir del id de un estudiante
    """
    filters = [models.ProjectStudent.student_id == student_id, models.ProjectStudent.active == True]
    db_project = (db.query(models.Project)
                .join(models.ProjectStudent, models.ProjectStudent.project_id == models.Project.id)
                .filter(*filters).first())
    return db_project

def get_students(project_id: int, db: Session, to_approve: bool = False):
    """
    Obtiene la lista de estudiantes actualmente inscritos en un proyecto
    """
    filters = []
    if to_approve:
        filters.append(models.User.total_hours >= 120)
    db_project = (db.query(models.User)
                .filter(*filters)
                .join(models.ProjectStudent, models.ProjectStudent.student_id == models.User.id)
                .filter(models.ProjectStudent.project_id == project_id)
                .filter(models.ProjectStudent.active == True).all())
    return db_project




