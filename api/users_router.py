import crud
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request, Header
from fastapi.security.api_key import APIKey
from fastapi.responses import FileResponse
from os import getcwd
from schemas.users_schema import User, row_to_schema
from schemas.other_schemas import UserIdentification, IdList
from db.db import get_db
from sqlalchemy.orm import Session
from core import utils
from core import responses
from core.config import settings
from core.messages import messages
from core import auth
from typing import List, Optional, Union
from db.enums import UserStatusEnum, RoleEnum



# crear router

users_router = APIRouter()

# ------------------------------ POST ------------------------------------------------
@users_router.post('/get_project_info_by_student', tags=['users'])
def get_project_info_by_student(identification: UserIdentification, db: Session = Depends(get_db), 
    api_key: APIKey = Depends(auth.get_api_key)):
    """
    Obtiene información del proyecto donde está inscrito un estudiante
    """
    # token = request.headers.get('Authorization')
    print(authorization)
    project_info = crud.users.get_project_info_by_student(identification.identification, db)
    if project_info == None:
        project_info = {}
    else:
        project_info = dict(project_info)
        project_info['task_list'] = crud.tasks.get_tasks_by_student(identification.identification, db)
    return project_info
    

@users_router.post('/get_user', tags=['users'])
def get_user(identification: UserIdentification, db: Session = Depends(get_db)):
    """
    Obtiene los datos de un usuario a partir de la cédula
    """
    user = crud.users.get_user_by_identification(identification.identification, db)
    return user


@users_router.post('/create_student', tags=['users'])
def create_student(user: User, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key),
    authorization: Union[str, None] = Header(default=None)):
    """
    Crear un estudiante
    """
    user_response = crud.users.create_user(user, RoleEnum.Student, db)
    return responses.USER_CREATED_SUCCESS



@users_router.post('/create_students', tags=['users'])
def create_students(users: List[User], db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key)):
    """
    Crear estudiantes a partir de una lista
    """
    response = crud.users.create_users_from_list(users, RoleEnum.Student, db)
    return response


@users_router.post('/create_tutor', tags=['users'])
def create_tutor(user: User, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key)):
    """
    Crear un tutor
    """
    user_response = crud.users.create_user(user, RoleEnum.Tutor, db)
    return responses.USER_CREATED_SUCCESS


@users_router.post('/create_tutors', tags=['users'])
def create_tutors(user: User, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key)):
    """
    Crear tutores a partir de una lista
    """
    response = crud.users.create_users_from_list(users, RoleEnum.Tutor, db)
    return response

@users_router.post('/create_students_from_file', tags=['users'])
async def upload_file(file: UploadFile=File(...), db: Session = Depends(get_db)
                    , api_key: APIKey = Depends(auth.get_api_key)):
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



@users_router.post('/create_tutors_from_file', tags=['users'])
async def upload_file(file: UploadFile=File(...), db: Session = Depends(get_db)
                    , api_key: APIKey = Depends(auth.get_api_key)):
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


# ------------------------------ UPDATE ------------------------------------------------

@users_router.put('/update_user/{identification}', tags=['users'])
def update_user(user: User, identification: str, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key)):
    """
    Actualiza los datos de un usuario 
    """
    users = crud.users.update_user(user, identification, db)
    return responses.USER_UPDATED_SUCCESS


@users_router.put('/update_student_status/{status}', tags=['users'])
def update_student_status(identification: UserIdentification, status: UserStatusEnum, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key)):
    """
    Actualiza el estatus de un estudiante
    """
    users = crud.users.update_student_status(identification.identification, status, db)
    return responses.USER_UPDATED_SUCCESS


@users_router.put('/update_students_status/{status}', tags=['users'])
def update_students_status(id_list: IdList, status: UserStatusEnum, db: Session = Depends(get_db)):
    """
    
    """
    crud.users.update_students_status(id_list.id_list, UserStatusEnum.Approved, db)
    return responses.USER_UPDATED_SUCCESS

# ------------------------------ GET ------------------------------------------------

@users_router.get('/get_students')
@users_router.get('/get_students/{status}', tags=['users'])
def get_students(status: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Obtener una lista de estudiantes con los siguientes campos
    Cédula, nombre, apellido, horas, proyecto, fecha de aprobación
    """
    if status == None:
        users = crud.users.get_students(db)
    elif status == 'No-asignado':             
        users = crud.users.get_students_without_project(db)
    elif status == 'Asignado':
        users = crud.users.get_students_with_project(db)
    elif status == 'Aprobado':
        users = crud.users.get_approved_students(db)
    elif status == 'Activo' or status == 'Inactivo':
        users = crud.users.get_students_by_status(db, status)
    else:
        raise HTTPException(status_code=400, detail=messages['incorrect_status'])
    return users




@users_router.get('/get_students_without_project', tags=['users'])
def get_students_without_project(db: Session = Depends(get_db)):
    """
    Obtener una lista de estudiantes que están activos pero
    no tienen proyecto asignado
    """
    users = crud.users.get_students_without_project(db)
    return users





@users_router.get('/get_tutors', tags=['users'])
def get_tutors(db: Session = Depends(get_db)):
    """
    Obtiene la lista de tutores
    """
    users = crud.users.get_tutors(db)
    return users











