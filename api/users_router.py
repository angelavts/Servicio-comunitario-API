import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from os import getcwd
from schemas.users_schema import User, row_to_schema
from db.db import get_db
from sqlalchemy.orm import Session
from core import utils
from core import responses
from core.config import settings
from core.messages import messages
from typing import List



# crear router

users_router = APIRouter()

@users_router.post('/create_student')
def create_student(user: User, db: Session = Depends(get_db)):
    """
    create a student
    """
    user_response = crud.users.create_user(user, 'Estudiante', db)
    return responses.USER_CREATED_SUCCESS



@users_router.post('/create_students')
def create_students(users: List[User], db: Session = Depends(get_db)):
    """
    create students from list
    """
    response = crud.users.create_users_from_list(users, 'Estudiante', db)
    return response


@users_router.post('/create_tutor')
def create_tutor(user: User, db: Session = Depends(get_db)):
    """
    create a tutor
    """
    user_response = crud.users.create_user(user, 'Tutor', db)
    return responses.USER_CREATED_SUCCESS


@users_router.post('/create_tutors')
def create_tutors(user: User, db: Session = Depends(get_db)):
    """
    create tutors from list
    """
    response = crud.users.create_users_from_list(users, 'Tutor', db)
    return response


@users_router.get('/user/{identification}')
def get_user(identification: str, db: Session = Depends(get_db)):
    """
    get user by identification
    """
    user = crud.users.get_user(identification, db)
    return user


@users_router.get('/students')
def get_students(db: Session = Depends(get_db)):
    """
    get students
    """
    users = crud.users.get_users('Estudiante', db)
    return users


@users_router.get('/students/{status}')
def get_students_by_status(status: str, db: Session = Depends(get_db)):
    """
    get students by status
    """
    users = crud.users.get_users_by_status('Estudiante', status, db)
    return users


@users_router.get('/tutors')
def get_tutors(db: Session = Depends(get_db)):
    """
    get a list of tutors
    """
    users = crud.users.get_users('Tutor', db)
    return users


@users_router.post('/create_students_from_file')
async def upload_file(file: UploadFile=File(...), db: Session = Depends(get_db)):
    """
    Crea estudiantes a partir de un archivo
    """
    # with open(getcwd() + file.filename, 'wb') as myfile:
    if not utils.is_valid_file(file.filename):
        raise HTTPException(400, detail=messages['invalid_document_type']) 

    # save file
    upload_path = utils.get_upload_path(file.filename)
    with open(upload_path, 'wb') as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()

    schema_list = utils.get_schema_list_from_file(upload_path, row_to_schema, settings.USERS_FILE_FORMAT)
    response = crud.users.create_users_from_list(schema_list, 'Estudiante', db)
    return response

@users_router.post('/create_tutors_from_file')
async def upload_file(file: UploadFile=File(...), db: Session = Depends(get_db)):
    """
    Crea estudiantes a partir de un archivo
    """
    # with open(getcwd() + file.filename, 'wb') as myfile:
    if not utils.is_valid_file(file.filename):
        raise HTTPException(400, detail=messages['invalid_document_type']) 

    # save file
    upload_path = utils.get_upload_path(file.filename)
    with open(upload_path, 'wb') as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()

    schema_list = utils.get_schema_list_from_file(upload_path, row_to_schema, settings.USERS_FILE_FORMAT)
    response = crud.users.create_users_from_list(schema_list, 'Tutor', db)
    return response






