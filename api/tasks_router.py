import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from os import getcwd
from schemas.tasks_schema import Task
from schemas.other_schemas import UserIdentification
from db.db import get_db
from db.enums import TaskStatusEnum
from sqlalchemy.orm import Session
from core import utils
from core import responses
from core.config import settings



CORRECT_COLUMNS = settings.TASK_FILE_FORMAT


# crear router

tasks_router = APIRouter()

# ---------------------------------------- POST ----------------------------------------------
# crear tarea
@tasks_router.post('/create_task', tags=['tasks'])
def create_task(task: Task, db: Session = Depends(get_db)):
    """
    create a task
    """
    task = crud.tasks.create(task, db)
    return responses.TASK_CREATED_SUCCESS

@tasks_router.post('/get_student_tasks', tags=['tasks'])
def get_student_tasks(student_identification: UserIdentification, db: Session = Depends(get_db)):
    """
    Obtener la lista de tareas de un estudiante en un proyecto especifico
    """
    tasks = crud.tasks.get_tasks_by_student(student_identification.identification, db)
    return tasks


@tasks_router.post('/get_tutor_tasks', tags=['tasks'])
def get_tutor_tasks(tutor_identification: UserIdentification, db: Session = Depends(get_db)):
    """
    Obtener la lista de tareas de las cuales se es tutor
    """
    tasks = crud.tasks.get_tasks_by_tutor(tutor_identification.identification, db)
    return tasks

# ---------------------------------------- UPDATE ----------------------------------------------

@tasks_router.put('/update_task_status/{task_id}/{status}', tags=['tasks'])
def update_task_status(task_id: int, status: TaskStatusEnum, db: Session = Depends(get_db)):
    """
    Update task status
    """
    tasks = crud.tasks.update_task_status(task_id, status, db)
    return responses.TASK_UPDATED_SUCCESS



# ---------------------------------------- GET ----------------------------------------------



@tasks_router.get('/get_project_tasks/{project_id}', tags=['tasks'])
def get_project_tasks(project_id: int, db: Session = Depends(get_db)):
    """
    Obtener la lista de tareas de un estudiante en un proyecto especifico
    """
    tasks = crud.tasks.get_tasks_by_project(project_id, db)
    return tasks










@tasks_router.get('/download/{file_name}')
async def download_file(file_name: str):
    """
    
    """
    return FileResponse(utils.get_upload_path(file_name), media_type='application/octet-stream', filename=file_name)