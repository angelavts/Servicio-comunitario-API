import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from os import getcwd
from schemas.projects_schema import Project
from db.db import get_db
from db.enums import ProjectStatusEnum
from sqlalchemy.orm import Session
from core import utils
from core import responses
from core.config import settings
from datetime import datetime

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

@projects_router.get('/get_projects_by_coordinator_status/{status}', tags=['projects'])
def get_projects_by_coordinator_status(project: Project, status: str, db: Session = Depends(get_db)):
    """
    get project list by coordinator and status
    """
    projects = crud.projects.get_projects_by_coordinator_status(project, status, db)
    return projects

@projects_router.get('/get_projects_by_career_status/{status}', tags=['projects'])
def get_projects_by_career_status(project: Project, status: str, db: Session = Depends(get_db)):
    """
    get project list by career and status
    """
    projects = crud.projects.get_projects_by_career_status(project, status, db)
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


