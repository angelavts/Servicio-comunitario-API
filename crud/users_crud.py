import pandas as pd
from db import db_models as models
from db.enums import RoleEnum, UserStatusEnum
from schemas.users_schema import User
from schemas.other_schemas import UserUpdate
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased 
from fastapi import status, HTTPException
from typing import List
from core import utils
from core import responses
from core.messages import messages
from datetime import datetime
from sqlalchemy import any_, exists, func, case
from itertools import groupby
from api import requests

# ------------------------------------------ POST ------------------------------------

def create_user(user: User, role: str, db: Session):
    """
    Crea un usuario 
    """
    db_user = db.query(models.User).filter(models.User.identification == user.identification).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail=messages['user_exists'])
    new_user = build_new_user(user, role, db) 
    try:
        db.add(new_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return new_user

def create_user_with_username(user: User, role: str, db: Session, token: str):
    """
    Crear un estudiante con usuario en autenticación
    """
    # dar formato a la cédula obtenida
    user.identification = utils.format_identication(user.identification)
    # registrar el usuario en el servicio de autenticación
    response = requests.create_user(user, RoleEnum.Student, token)
    username = None
    # tratar de obtener el username 
    try:
        username = response['username']
    except Exception as e:
        print(e)
    if username != None:
        # en caso de que exista el username, se procede a registrar el usuario
        new_user = create_user(user, RoleEnum.Student, db)
        # si el registro es exitoso, se convierte la respuesta en diccionario y se agrega el username
        response = {
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "identification": new_user.identification,
            "username": username
        }
    else:      
        print(response) 
        message = "" 
        try:
            # no existe username, significa que hay un error en autenticación
            # tratar de enviar error con el mensaje de error de autenticación
            message = response['message']
        except Exception as e:
            print(e) 
            message = messages['internal_error']  
        raise HTTPException(status_code=500, detail=message)
    return response

    
def create_users_from_list(users: List[User], role: str, db: Session):
    """
    Crear usuarios a partir de una lista
    """
    response = {}
    successful = []
    failed = []
    for user in users:
        # se debe verificar que el formato de cédula es correcto
        if utils.is_valid_identication(user.identification):
            new_user = build_new_user(user, role, db)
            try:
                db.add(new_user)
                db.commit()
                successful.append(user)
            except Exception as e:
                db.rollback()
                failed.append({'User': user, 'detail': str(e)})
        else:
            failed.append({'User': user, 'detail': messages['invalid_id_format']})

    response['successful'] = successful
    response['failed'] = failed        
    return response

def create_users_with_username(users: List[User], role: str, db: Session, token: str):
    """
    Crear usuarios a partir de una lista, también se registrarán en autenticación
    """
    response = requests.create_users(users, role, token)
    # intentar extraer la lista de usuarios
    auth_list = []
    try:
        auth_list = response['users']
    except Exception as e:
        print(e)
        # si no se tiene la lista de usuarios es porque no se registró ninguno
        response = {
            "successful": [],
            "failed": users
        }

    if auth_list:
        # ya que se tiene una lista de usuarios registrados en autenticación
        # se procede a hacer el registro en la base de datos
        successful = []
        failed = []
        # convertir la lista de usuarios registrados en un dataframe
        df_users = pd.DataFrame.from_records(auth_list)
        # recorrer la lista de usuarios que se pudieron registrar en autenticación
        for user in users:
            # buscar este usuario en el dataframe
            user_data = df_users[df_users['identification'] == user.identification]
            if not user_data.empty:
                # si existe el usuario, es porque se pudo registrar en autenticación, se
                # procede a registrar el usuario en la bd
                new_user = build_new_user(user, role, db)
                try:
                    db.add(new_user)
                    db.commit()
                    # se agrega el usuario a la lista de exitodos y
                    # se incluye el username obtenido de autenticación
                    response_user = user.dict()
                    response_user['username'] = user_data['username'].values[0]
                    successful.append(response_user)
                except Exception as e:
                    db.rollback()
                    failed.append(user)
            else:
                # si no se registró el usuario en autenticación,
                # se devuelven sus datos en la lista de fallidos
                failed.append(user)
        response = {
            'successful' : successful,
            'failed' : failed 
        }      
    return response

# ------------------------------------------ UPDATE ------------------------------------

def update_hours(user_id: int, hours: int, db: Session):
    # buscar estudiante en la bd
    db_user = get_user_by_id(user_id, db)
    # sumar las horas
    if db_user.total_hours != None:
        db_user.total_hours += hours
    else:
        db_user.total_hours = hours
    try:
        db.add(db_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        print(e)



def update_user(user: UserUpdate, token: str, db: Session):
    """
    Crea un usuario 
    """
    # buscar el usuario por cédula
    db_user = get_user_by_identification(user.identification, db)
    # enviar error si el usuario no existe
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])

    is_modified_in_auth_service = True
    # modificar correo en caso de que se tenga el dato
    if user.email != None:
        db_user.email = user.email
        response = requests.update_user(user, token)
        print(response)
        is_modified_in_auth_service = response["ok"]
    
    if is_modified_in_auth_service:
        # modificar nombre en caso de que se tenga el dato
        if user.first_name != None:
            db_user.first_name = user.first_name
        # modificar apellido en caso de que se tenga el dato
        if user.last_name != None:
            db_user.last_name = user.last_name

        # modificar telefono en caso de que se tenga el dato
        if user.phone != None:
            db_user.phone = user.phone
        # modificar status, en caso de que se tenga el dato
        if user.status != None:
            db_user.status = user.status
        # modificar carrera, en caso de que se tenga el dato
        if user.career != None:
            # revisar si existe la carrera 
            db_career = db.query(models.Career).filter(models.Career.name == user.career).first()
            if db_career != None:
                db_user.career_id = db_career.id
        # modificar proyecto en caso de que sea necesario
        if user.project_id != None:
            # verificar que el proyecto existe
            db_project = db.query(models.Project).filter(models.Project.id == user.project_id).first()
            if db_project is None:
                raise HTTPException(status_code=400, detail=messages['project_not_exists'])
            update_project(db_user, db_project, db)
        # guardar cambios en la db 
        try:
            db.add(db_user)
            db.commit()        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=messages['internal_error'])
    else:
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_user

def update_project(user: models.User, db_project: models.Project, db: Session):
    """
    Actualiza el proyecto de un estudiante
    """

    # buscar el proyecto que tiene activo actualmente 
    filters = [models.ProjectStudent.student_id == user.id, models.ProjectStudent.active == True]
    db_project_active = db.query(models.ProjectStudent).filter(*filters).first()

    if db_project_active is not None:
        # desactivar el proyecto que tiene activo actualmente
        db_project_active.active = False
        try:
            # actualizar base de datos
            db.add(db_project_active)
            db.commit()        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=messages['internal_error'])
    
    # buscar la relación del proyecto que se quiere crear
    filters = [models.ProjectStudent.project_id == db_project.id, 
               models.ProjectStudent.student_id == user.id, models.ProjectStudent.active == True]
    db_project_new = db.query(models.ProjectStudent).filter(*filters).first()

    if db_project_new is not None:
        # si existe, activar
        db_project_new.active = True
    else:
        # si no existe, crear una nueva
        db_project_new = models.ProjectStudent(
            project_id=db_project.id,
            student_id=user.id,
            active=True
        ) 
    # guardar el cambio en la bd
    try:
        # actualizar base de datos
        db.add(db_project_new)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_project_new


def enroll_students_in_project(identifications: List[str], project_id: int,  db: Session):
    """
        Inscribe a todos los estudiantes dados en una lista en un proyecto especifico
    """
    success = []
    failed = []
    # verificar que el proyecto existe
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=400, detail=messages['project_not_exists'])

    for identification in identifications: 
        # buscar el estudiante en la bd
        db_user = get_user_by_identification(identification, db)
        if db_user is None:
            failed.append(identification)
        else:
            try:
                # inscribir estudiante en el proyecto indicado
                update_project(db_user, db_project, db)  
                success.append(identification)    
            except Exception as e:
                print(e)
                failed.append(identification) 
    
    if not failed:
        response = responses.STUDENTS_ENROLLED
    else:
        response = {
            'successful' : success,
            'failed' : failed 
        }  
    return response
        



def update_student_status(identification: str, status: str, db: Session):
    """
    Actualiza el status de un estudiante
    """
    db_user = db.query(models.User).filter(models.User.identification == identification).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])
    # cambiar el estatus
    db_user.status = status
    # si el estudiante es aprobado, se coloca su fecha de finalización
    date_approval = None
    if status == UserStatusEnum.Approved:
        date_approval = datetime.now()     
    db_user.date_approval = date_approval
    try:
        # actualizar base de datos
        db.add(db_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_user


def update_students_status(id_list: list, status: str, db: Session):
    """
        Actualiza el status de varios estudiantes 
    """
    successful = []
    failed = []

    for id_student in id_list:
        db_student = db.query(models.User).filter(models.User.id == id_student).first()
        if db_student != None:
            # cambiar el estatus
            db_student.status = status
            # si el estudiante es aprobado, se coloca su fecha de finalización
            date_approval = None
            if status == UserStatusEnum.Approved:
                date_approval = datetime.now()     
            db_student.date_approval = date_approval
            try:
                # actualizar base de datos
                db.add(db_student)
                db.commit() 
                successful.append(id_student)
            except Exception as e:
                print(e)
                failed.append(id_student)
                db.rollback()
        else:
            failed.append(id_student)
    
    response = {}
    response['successful'] = successful
    response['failed'] = failed        
    return response

# ------------------------------------------ GET ------------------------------------

def is_user_in_db(identification: str, db: Session):
    """
    Verifica si el usuario existe en la base de datos
    """
    # buscar el id del usuario
    db_user =  db.query(models.User).filter(models.User.identification == identification).first()
    return db_user != None


def get_user_by_identification(identification: str, db: Session):
    """
    Busca un usuario la base de datos
    """
    # buscar el id del usuario
    db_user =  db.query(models.User).filter(models.User.identification == identification).first()
    return db_user

def get_user_by_id(user_id: int, db: Session):
    """
    Busca un usuario la base de datos
    """
    # buscar el id del usuario
    db_user =  db.query(models.User).filter(models.User.id == user_id).first()
    return db_user


def get_user_info_by_identification(identification: str, db: Session):
    """
    Obtiene un usuario a partir de la cédula
    """
    db_user = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    models.User.total_hours, 
                    models.User.status,
                    models.User.date_approval,   
                    models.User.email,   
                    models.User.phone,                   
                    models.Career.name.label('career_name'))
                .outerjoin(models.Career, models.Career.id == models.User.career_id)
                .filter(models.User.identification == identification).first())
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])
    return db_user



def get_students(db: Session, status: str=None):
    """
    Obtener una lista de estudiantes con los siguientes campos
    Cédula, nombre, apellido, horas, estatus, proyecto, fecha de aprobación
    """
    filters = [models.User.role == RoleEnum.Student]
    if status is not None:
        filters = [models.User.status == status]

    projects_alias = aliased(models.Project, name='project')
    career_alias = aliased(models.Career, name='career')
    db_students = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    models.User.phone,
                    models.User.email,
                    models.User.total_hours, 
                    models.User.status,
                    models.User.date_approval,
                    career_alias, 
                    projects_alias)
                .filter(*filters)
                .outerjoin(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                .filter(models.ProjectStudent.active)
                .outerjoin(projects_alias, projects_alias.id == models.ProjectStudent.project_id)   
                .outerjoin(career_alias, career_alias.id == models.User.career_id)                
                .all())
    return db_students

def get_approved_students(db: Session):
    """
    Obtener una lista de estudiantes con los siguientes campos
    Cédula, nombre, apellido, horas, estatus, proyecto, fecha de aprobación
    """
    filters = [models.User.role == RoleEnum.Student, models.User.status == UserStatusEnum.Approved]
    print("get approved students")
    projects_alias = aliased(models.Project, name='project')
    career_alias = aliased(models.Career, name='career')
    db_students = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    career_alias.name.label('career'), 
                    projects_alias.name.label('project'),
                    models.User.total_hours, 
                    models.User.date_approval)
                .filter(*filters)
                .outerjoin(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                .filter(models.ProjectStudent.active)
                .outerjoin(projects_alias, projects_alias.id == models.ProjectStudent.project_id)   
                .outerjoin(career_alias, career_alias.id == models.User.career_id)                
                .all())
    return db_students

def get_students_with_project(db: Session):
    """
    Obtener una lista de estudiantes con los siguientes campos
    Cédula, nombre, apellido, horas, estatus, proyecto, fecha de aprobación
    """
    filters = [models.User.role == RoleEnum.Student, models.User.status == UserStatusEnum.Active]

    projects_alias = aliased(models.Project, name='project')
    career_alias = aliased(models.Career, name='career')
    db_students = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    models.User.phone,
                    models.User.email,
                    models.User.status,
                    career_alias.name.label('career'), 
                    projects_alias.name.label('project'),
                    models.User.total_hours)
                .filter(*filters)
                .outerjoin(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                .filter(models.ProjectStudent.active)
                .outerjoin(projects_alias, projects_alias.id == models.ProjectStudent.project_id)   
                .outerjoin(career_alias, career_alias.id == models.User.career_id)                
                .all())
    return db_students


def get_students_by_status(db: Session, status: str):
    """
    Obtener una lista de estudiantes activos o inactivos
    """
    filters = [models.User.role == RoleEnum.Student, models.User.status == status]
    career_alias = aliased(models.Career, name='career')
    db_students = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    models.User.phone,
                    models.User.email,
                    models.User.status,
                    career_alias.name.label('career'),
                    models.User.total_hours
                    )
                .filter(*filters)
                .outerjoin(career_alias, career_alias.id == models.User.career_id)                
                .all())
    return db_students

def get_students_without_project(db: Session):
    """
    Obtener una lista de estudiantes que no tienen proyecto activo
    es decir, que no existen en una relación ProjectStudent o que
    todas sus relaciones tienen active en falso 
    """
    filters = [models.User.role == RoleEnum.Student, models.User.status == UserStatusEnum.Active]
    career_alias = aliased(models.Career, name='career')
    db_user = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name, 
                    models.User.phone,
                    models.User.email,
                    models.User.status,                     
                    career_alias.name.label('career'), 
                    models.User.total_hours,
                    func.count(models.ProjectStudent.active)
                )
                .filter(*filters)
                .outerjoin(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                .group_by(career_alias, models.User.id)
                .having(func.count(1).filter(models.ProjectStudent.active) == 0)
                .outerjoin(career_alias, career_alias.id == models.User.career_id)
                ).all()            
    return db_user


def get_users_by_role(role: str, db: Session):
    """
    Obtiene una lista de usuarios según el rol indicado
    """
    db_users = (db.query(models.User.id,
                         models.User.identification, 
                         models.User.fullname,
                         models.User.total_hours, 
                         models.User.phone,
                         models.User.email,
                         models.User.status, 
                         models.User.role,
                         models.User.career_id,                      
                        models.Career.name.label('career_name'))
                    .outerjoin(models.Career, models.Career.id == models.User.career_id)
                .filter(models.User.role == role)               
                .all())
    return db_users

def get_tutors(db: Session):
    """
    Obtiene una lista de usuarios según el rol indicado
    """
    career_alias = aliased(models.Career, name='career')
    db_users = (db.query(models.User.id,
                         models.User.identification, 
                         models.User.first_name, 
                         models.User.last_name,              
                         models.User.phone,
                         models.User.email,       
                         career_alias.name)
                    .outerjoin(career_alias, career_alias.id == models.User.career_id)
                .filter(models.User.role == RoleEnum.Tutor)               
                .all())
    return db_users



def get_project_info_by_student(identification: str, db: Session):
    """5
        Busca información del proyecto donde se encuentra inscrito un estudiante    
    """
    coordinator = aliased(models.User, name='coordinator')
    project_info = (db.query(
                    models.Project.id,
                    models.Project.name,
                    models.Project.description, 
                    models.Project.date_start, 
                    coordinator.fullname.label('coordinator'))                
                .join(models.ProjectStudent, models.Project.id == models.ProjectStudent.project_id)
                .join(models.User, models.User.id == models.ProjectStudent.student_id)
                .filter(models.User.identification == identification)
                .filter(models.ProjectStudent.active)
                .join(coordinator, coordinator.id == models.Project.coordinator_id)
                .first())    
    return project_info


# ------------------------------------------ TOOLS ------------------------------------

def build_new_user(user: User, role: str, db: Session):
    # revisar si existe la carrera 
    db_career = db.query(models.Career).filter(models.Career.name == user.career).first()

    new_user = models.User(
        identification=user.identification,
        first_name=user.first_name,
        last_name=user.last_name,            
        role = role,
        career_id = db_career.id if db_career != None else None,
        email = user.email,
        phone = user.phone
    )  
    return new_user



