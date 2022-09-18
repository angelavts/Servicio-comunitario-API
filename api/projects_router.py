import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from os import getcwd
from schemas.projects_schema import Project, row_to_schema
from db.db import get_db
from db.enums import ProjectStatusEnum
from sqlalchemy.orm import Session
from core import utils
from core import responses
from core.config import settings
from datetime import datetime
from typing import Optional, List
from fastapi.security.api_key import APIKey
from core.messages import messages
from core import auth

# crear router

projects_router = APIRouter()

# crear un proyecto
@projects_router.post('/create_project', tags=['projects'])
def create_project(project: Project, db: Session = Depends(get_db)):
    """
    create a project
    """
    project = crud.projects.create(project, db)
    return responses.PROJECT_CREATED_SUCCESS

# actualizar proyectos
@projects_router.put('/update_project_status/{project_id}/{status}', tags=['projects'])
def update_project_status(project_id: int, status: str, db: Session = Depends(get_db)):
    """
    Update project status
    """
    project = crud.projects.update_project_status(project_id, status, db)
    return responses.PROJECT_UPDATED_SUCCESS

@projects_router.put('/update_project_date_end/{project_id}/{date}', tags=['projects'])
def update_project_date_end(project_id: int, date: datetime, db: Session = Depends(get_db)):
    """
    Update project status
    """
    project = crud.projects.update_project_date_end(project_id, date, db)
    return responses.PROJECT_UPDATED_SUCCESS

# obtener proyectos
@projects_router.get('/get_projects_by_status/{status}', tags=['projects'])
def get_projects_by_status(status: ProjectStatusEnum, db: Session = Depends(get_db)):
    """
    get project list by status
    """
    projects = crud.projects.get_projects_by_status(status, db)
    return projects

@projects_router.get('/get_projects_by_coordinator_status/{status}/{coordinator}', tags=['projects'])
def get_projects_by_coordinator_status(coordinator_id: int, status: ProjectStatusEnum, db: Session = Depends(get_db)):
    """
    get project list by coordinator and status
    """
    projects = crud.projects.get_projects_by_coordinator_status(coordinator_id, status, db)
    return projects

@projects_router.get('/get_projects_by_career_status/{status}/{career}', tags=['projects'])
def get_projects_by_career_status(career: int, status: ProjectStatusEnum, db: Session = Depends(get_db)):
    """
    get project list by career and status
    """
    projects = crud.projects.get_projects_by_career_status(career, status, db)
    return projects

@projects_router.get('/get_project/{project_id}', tags=['projects'])
def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    get a project
    """
    project = crud.projects.get_project(project_id, db)
    return project


@projects_router.get('/get_active_project_by_student_id/{student_id}', tags=['projects'])
def get_active_project_by_student_id(student_id: int, db: Session = Depends(get_db)):
    """
    Obtener el proyecto activo de un estudiante a partir de un id
    """
    project = crud.projects.get_active_project_by_student_id(student_id, db)
    return project

@projects_router.get('/get_students/{project_id}', tags=['projects'])
def get_students(project_id: int, db: Session = Depends(get_db)):
    """
    Obtiene la lista de estudiantes actualmente inscritos en un proyecto
    """
    project = crud.projects.get_students(project_id, db)
    return project


@projects_router.get('/get_students_to_approval/{project_id}', tags=['projects'])
def get_students_to_approval(project_id: int, db: Session = Depends(get_db)):
    """
    Obtiene la lista de estudiantes actualmente inscritos en un proyecto que
    tienen más de 120 horas
    """
    project = crud.projects.get_students(project_id, db, to_approve=True)
    return project

@projects_router.get('/get_active_projects', tags=['projects'])
def get_active_projects(db: Session = Depends(get_db)):
    """
    get a list of active projects
    """
    projects = crud.projects.get_active_projects(db)
    return projects

@projects_router.get('/get_all_projects')
@projects_router.get('/get_all_projects/by_status/{status}', tags=['projects'])
def get_all_projects(status: Optional[ProjectStatusEnum] = None, db: Session = Depends(get_db)):
    """
    Obtiene una lista de proyectos
    """
    projects = crud.projects.get_all_projects(db, status)
    return projects


@projects_router.post('/create_projects_from_file', tags=['projects'])
async def upload_file(file: UploadFile=File(...), db: Session = Depends(get_db)
                    , api_key: APIKey = Depends(auth.get_api_key)):
    """
    Crea proyectos a partir de un archivo
    """
    if not utils.is_valid_file(file.filename):
        raise HTTPException(400, detail=messages['invalid_document_type']) 
    # save file
    upload_path = utils.get_upload_path(file.filename)
    with open(upload_path, 'wb') as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    schema_list = utils.get_schema_list_from_file(upload_path, row_to_schema, settings.PROJECTS_FILE_FORMAT)
    response = crud.projects.create_projects_from_list(schema_list, db)
    return response

@projects_router.post('/create_projects', tags=['projects'])
def create_projects(projects: List[Project], db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key)):
    """
    Crear proyectos a partir de una lista
    """
    response = crud.projects.create_projects_from_list(projects, db)
    return response