from db import db_models as models
from schemas.projects_schema import Project
from schemas.users_schema import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List
from core.messages import messages
from core.config import settings
from datetime import datetime
from db.enums import ProjectStatusEnum, RoleEnum
from sqlalchemy import func, case
import crud.users_crud as users_crud
from schemas.other_schemas import ProjectUpdate



# --------------------------------------------- TOOLS ------------------------------------------------------------
def get_project_by_id(project_id: str, error_message: str, db: Session):
    # buscar el id del estudiante
    db_user =  db.query(models.Project).filter(models.Project.id == project_id).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail=messages[error_message])
    
    return db_user


def get_career_by_name(name: str, error_message: str, db: Session):
    # buscar el id de la carrera 
    db_career =  db.query(models.Career).filter(models.Career.name == name).first()
    if db_career is None:
        raise HTTPException(status_code=400, detail=messages[error_message])
    return db_career


def create_new_coordinator(project: Project, db: Session):
    # Crea un nuevo coordinador
    new_user = User(
            identification = project.coordinator_identification,
            first_name = project.coordinator_first_name,
            last_name = project.coordinator_last_name,
            career = project.coordinator_career,
            email = project.coordinator_email,
            phone = project.coordinator_phone
        ) 
    return users_crud.create_user(new_user, RoleEnum.Coordinator, db)

def convert_date(date: str):
    """
    Convierte una fecha en formato dd/mm/aaaa a datetime
    """
    return datetime.strptime(date, '%d/%m/%Y')
# --------------------------------------------- POST ------------------------------------------------------------
def create(project: Project, db: Session):
    """
    Crea un proyecto 
    """
    # buscar el id del coordinador
    coordinator = users_crud.get_user_by_identification(project.coordinator_identification, db)
    if coordinator is None:          
        coordinator = create_new_coordinator(project, db)
    
    # buscar el id de la carrera
    career = get_career_by_name(project.career, 'career_not_exists', db)

    # Validacion de proyectos duplicados
    db_project = (
        db.query(models.Project).filter(models.Project.name == project.name).first()
    )
    if db_project is not None:
        raise HTTPException(status_code=400, detail=messages['project_exists'])

    new_project = models.Project(
        name=project.name,
        description=project.description,
        date_start=convert_date(project.date_start),
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

def create_projects_from_list(projects: List[Project], db: Session):
    """
    Crear usuarios a partir de una lista
    """
    response = {}
    successful = []
    failed = []
    for project in projects:
        try:
            new_project = create(project, db)
            successful.append(project)
        except Exception as e:
            failed.append(project)
    response['successful'] = successful
    response['failed'] = failed        
    return response

# --------------------------------------------- UPDATE ------------------------------------------------------------
def update_project(project_id: int, project: ProjectUpdate, db: Session):
    """
    Actualizar un proyecto 
    """
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=400, detail=messages['project_not_exists'])

    # cambiar descripcion del proyecto
    if project.description != None and project.description != db_project.description:
        db_project.description = project.description
    
    # cambiar fecha de culminacion del proyecto
    if project.date_end != None and project.date_end != db_project.date_end:
        db_project.date_end = project.date_end

    # cambiar status del proyecto
    if project.status != None and project.status != db_project.status:
        db_project.status = project.status

    # ultima actualizacion
    db_project.updated_at = datetime.now()
    
    try:
        db.add(db_project)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return project

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
                         models.User.id.label('coordinator_id'),
                         models.User.first_name.label('coordinator_first_name'), 
                         models.User.last_name.label('coordinator_last_name'), 
                         models.Career.name.label('career_name'))
                         .join(models.User, models.User.id == models.Project.coordinator_id)
                         .join(models.Career, models.Career.id == models.Project.career_id)
                         .filter(models.Project.status == status)               
                ).all()
    return projects

def get_projects_by_coordinator_status(coordinator_id: int, status: str, db: Session):
    """
    Obtiene una lista de proyectos de un coordinador especifico por status
    """

    projects = (db.query(models.Project.id,
                         models.Project.name, 
                         models.Project.date_start, 
                         models.Project.date_end,
                         models.User.id.label('coordinator_id'),
                         models.User.first_name.label('coordinator_first_name'), 
                         models.User.last_name.label('coordinator_last_name'), 
                         models.Career.name.label('career_name'))
                         .join(models.User, models.User.id == models.Project.coordinator_id)
                         .join(models.Career, models.Career.id == models.Project.career_id)
                         .filter(models.Project.coordinator_id == coordinator_id and models.Project.status == status)               
                ).all()
    return projects

def get_projects_by_career_status(career_id: int, status: str, db: Session):
    """
    Obtiene una lista de proyectos de una carrera especifica por status
    """

    projects = (db.query(models.Project.id,
                         models.Project.name, 
                         models.Project.date_start, 
                         models.Project.date_end,
                         models.User.id.label('coordinator_id'),
                         models.User.first_name.label('coordinator_first_name'), 
                         models.User.last_name.label('coordinator_last_name'), 
                         models.Career.name.label('career_name'))
                         .join(models.User, models.User.id == models.Project.coordinator_id)
                         .join(models.Career, models.Career.id == models.Project.career_id)
                         .filter(models.Project.career_id == career_id and models.Project.status == status)               
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
        filters.append(models.User.total_hours >= settings.TOTAL_HOURS)
        filters.append(models.User.status == UserStatusEnum.Active)
    db_project = (db.query(models.User.id,
                           models.User.identification,
                           models.User.first_name,
                           models.User.last_name,
                           models.Career.name.label('career'),
                           models.User.total_hours)
                .filter(*filters)
                .join(models.ProjectStudent, models.ProjectStudent.student_id == models.User.id)
                .filter(models.ProjectStudent.project_id == project_id)
                .filter(models.ProjectStudent.active == True)
                .outerjoin(models.Career, models.User.career_id == models.Career.id).all())
    return db_project

def get_active_projects(db: Session):
    """
    Obtiene una lista de proyectos activos
    """
    projects = (db.query(models.Project.id,
                         models.Project.name, 
                         models.Project.description, 
                         models.Project.date_start,
                         models.Project.status,
                         func.count(case([(models.ProjectStudent.active == True, 1)])).label('student_count'))
                         .outerjoin(models.ProjectStudent, models.Project.id == models.ProjectStudent.project_id)
                         .filter(models.Project.status == ProjectStatusEnum.Active)
                         .group_by(models.Project.id)              
                ).all()

    return projects

def get_all_projects(db: Session, status: str=None):
    """
    Obtiene una lista de proyectos
    """
    filter = []
    if status:
        filter = [models.Project.status == status]
    projects = (db.query(models.Project.id,
                         models.Project.name, 
                         models.Project.description, 
                         models.Project.date_start,
                         models.Project.date_end,
                         models.Project.status)
                         .filter(*filter)            
                ).all()
    return projects




