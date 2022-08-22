import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from os import getcwd
from schemas.users_schema import User, row_to_schema
from db.db import get_db
from sqlalchemy.orm import Session
from core import utils
from core.config import settings
from core import responses


CORRECT_COLUMNS = settings.STUDENTS_FILE_FORMAT


# crear router

users_router = APIRouter()


# crear tarea
@users_router.post('/create_student', tags=['users'])
def create_users(user: User, db: Session = Depends(get_db)):
    """
    create a student
    """
    user = crud.users.create_student(user, db)
    return responses.USER_CREATED_SUCCESS

@users_router.get('/user/{identification}', tags=['users'])
def list_users(identification: str, db: Session = Depends(get_db)):
    """
    create students
    """
    # user = crud.users.create(user, db)
    is_valid = utils.is_valid_identication(identification)

    return 'Es válida' if is_valid else 'No es válida'


# crear tareas a partir de archivo
@users_router.post('/upload')
async def upload_file(file: UploadFile=File(...), db: Session = Depends(get_db)):
    """
    create users from a file
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

    schema_list = utils.get_schema_list_from_file(upload_path, row_to_schema, CORRECT_COLUMNS)
    response = crud.users.create_from_list(schema_list, db)
    return response

