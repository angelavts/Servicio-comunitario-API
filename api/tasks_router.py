import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from os import getcwd
from schemas.tasks_schema import Task
from db.db import get_db
from sqlalchemy.orm import Session
from core import utils
from core import responses
from core.config import settings


CORRECT_COLUMNS = settings.TASK_FILE_FORMAT


# crear router

tasks_router = APIRouter()


# crear tarea
@tasks_router.post('/', tags=['task'])
def create_task(task: Task, db: Session = Depends(get_db)):
    """
    create a task
    """
    task = crud.tasks.create(task, db)
    return responses.TASK_CREATED_SUCCESS


@tasks_router.get('/{project_id}/{student_identification}', tags=['task'])
def create_task(project_id: int, student_identification: str, db: Session = Depends(get_db)):
    """
    get task list of a student
    """
    tasks = crud.tasks.get_tasks_from_student(project_id, student_identification, db)
    return tasks



@tasks_router.put('/{task_id}', tags=['task'])
def create_task(task_id: int, status: str, db: Session = Depends(get_db)):
    """
    Update task status
    """
    tasks = crud.tasks.update_task_status(task_id, status, db)
    return responses.TASK_UPDATED_SUCCESS


@tasks_router.get('/download/{file_name}')
async def download_file(file_name: str):
    """
    
    """
    return FileResponse(utils.get_upload_path(file_name), media_type='application/octet-stream', filename=file_name)