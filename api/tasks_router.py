import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from os import getcwd
from schemas.tasks_schema import Task
from db.db import get_db
from sqlalchemy.orm import Session
from core import utils
from core.config import settings


CORRECT_COLUMNS = settings.TASK_FILE_FORMAT


# crear router

tasks_router = APIRouter()


# crear tarea
@tasks_router.post('/', response_model=Task, tags=['task'])
def create_task(task: Task, db: Session = Depends(get_db)):
    """
    create a task
    """
    task = crud.tasks.create(task, db)
    return task


# crear tareas a partir de archivo
@tasks_router.post('/upload')
async def upload_file(file: UploadFile=File(...), db: Session = Depends(get_db)):
    """
    create tasks from a file
    """
    # with open(getcwd() + file.filename, 'wb') as myfile:
    if not utils.is_valid_file(file.filename):
        raise HTTPException(400, detail="Invalid document type") 

    # save file
    upload_path = utils.get_upload_path(file.filename)
    with open(upload_path, 'wb') as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()

    schema_list = utils.get_schema_list_from_file(upload_path, Task, CORRECT_COLUMNS)
    response = crud.tasks.create_from_list(schema_list, db)
    return response


@tasks_router.get('/download/{file_name}')
async def download_file(file_name: str):
    """
    
    """
    return FileResponse(utils.get_upload_path(file_name), media_type='application/octet-stream', filename=file_name)