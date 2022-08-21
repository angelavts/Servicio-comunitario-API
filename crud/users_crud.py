from db import db_models as models
from schemas.users_schema import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List


def create_student(user: User, db: Session):
    """
    Crea un usuario 
    """
    db_user = db.query(models.User).filter(models.User.identification == user.identification).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Item already exists")

    new_user = models.User(
        identification=user.identification,
        first_name=user.first_name,
        last_name=user.last_name,            
        role = 'Pendiente'
    ) 

    db.add(new_user)
    db.commit()

    return new_user


def create_from_list(users: List[User], db: Session):
    """
    Crear usuarios a partir de una lista
    """
    response = {}
    successful = []
    failed = []
    for user in users:

        new_user = models.User(
            identification=user.identification,
            first_name=user.first_name,
            last_name=user.last_name,            
            role = 'Estudiante'
        ) 
        try:
            db.add(new_user)
            db.commit()
            successful.append(new_user.first_name)
        except Exception as e:
            db.rollback()
            failed.append([new_user.first_name, str(e)])

    response['Users added'] = len(successful)
    response['Users failed'] = len(failed)
    response['successful'] = successful
    response['failed'] = failed
        
    return response
