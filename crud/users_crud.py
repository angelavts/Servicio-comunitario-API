from db import db_models as models
from db.enums import role_enum
from schemas.users_schema import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List
from core import utils
from core.messages import messages





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

def update_user(user: User, identification: str, db: Session):
    """
    Crea un usuario 
    """
    db_user = db.query(models.User).filter(models.User.identification == user.identification).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])
    # revisar si existe la carrera 
    db_career = db.query(models.Career).filter(models.Career.name == user.career).first()
    # cambiar datos del usuario
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.career_id = db_career.id
    try:
        db.add(db_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_user

def update_student_status(identification: str, status: str, db: Session):
    """
    Crea un usuario 
    """
    db_user = db.query(models.User).filter(models.User.identification == identification).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])
    # cambiar el estatus
    db_user.status = status
    try:
        # actualizar base de datos
        db.add(db_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_user


def get_user(identification: str, db: Session):
    """
    Obtiene un usuario 
    """
    db_user = (db.query(
                    models.User.id,
                    models.User.identification, 
                    models.User.first_name, 
                    models.User.last_name,
                    models.User.total_hours, 
                    models.User.status, 
                    models.Career.name.label('career'))
                .join(models.Career, models.User.career_id == models.Career.id)
                .filter(models.User.identification == identification).first())
    if db_user is None:
        raise HTTPException(status_code=400, detail=messages['user_not_exists'])
    return db_user

def get_users_by_status(role: str, status: str, db: Session):
    """
    Obtiene una lista de usuarios con un status específico
    """
    if status not in role_enum:
        raise HTTPException(status_code=400, detail=messages['incorrect_status'])

    db_users = (db.query(models.User)
                  .filter(models.User.role == role)
                  .filter(models.User.status == status)                  
               ).all()
    return db_users


def get_users(role: str, db: Session):
    """
    Obtiene una lista de usuarios
    """
    db_users = (db.query(models.User.id,
                         models.User.identification, 
                         models.User.first_name, 
                         models.User.last_name,
                         models.User.total_hours, 
                         models.User.status, 
                         models.User.role
                ).filter(models.User.role == role)               
                ).all()
    return db_users



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

def build_new_user(user: User, role: str, db: Session):
    # revisar si existe la carrera 
    db_career = db.query(models.Career).filter(models.Career.name == user.career).first()

    new_user = models.User(
        identification=user.identification,
        first_name=user.first_name,
        last_name=user.last_name,            
        role = role,
        career_id = db_career.id
    )  
    return new_user



