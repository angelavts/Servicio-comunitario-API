from db import db_models as models
from schemas.users_schema import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List
from core import utils


def create_student(user: User, db: Session):
    """
    Crea un usuario 
    """
    db_user = db.query(models.User).filter(models.User.identification == user.identification).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Item already exists")
    new_user = build_new_user(user, 'Estudiante', db) 
    try:
        db.add(new_user)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return new_user


def create_from_list(users: List[User], db: Session):
    """
    Crear usuarios a partir de una lista
    """
    response = {}
    successful = []
    failed = []
    for user in users:
        # se debe verificar que el formato de cédula es correcto
        identificacion = utils.validate_and_convert_identication(user.identification)
        if identificacion is not None:
            # Colocar cédula en el formato correcto
            user.identification = identificacion
            new_user = build_new_user(user, 'Estudiante', db)
            try:
                db.add(new_user)
                db.commit()
                successful.append(user)
            except Exception as e:
                db.rollback()
                failed.append({'user': new_user, 'detail': str(e)})
        else:
            failed.append([user, 'Invalid identification format'])

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
        career = db_career
    )  
    return new_user

