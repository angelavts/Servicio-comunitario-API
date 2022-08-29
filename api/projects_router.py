import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from os import getcwd
from schemas.projects_schema import Project
from db.db import get_db
from sqlalchemy.orm import Session
from core import utils
from core import responses
from core.config import settings

# crear router

projects_router = APIRouter()


# crear tarea
@projects_router.post('/', tags=['projects'])
def create_project(project: Project, db: Session = Depends(get_db)):
    """
    create a project
    """
    task = crud.projects.create(project, db)
    return responses.TASK_CREATED_SUCCESS