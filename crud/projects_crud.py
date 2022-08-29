from db import db_models as models
from schemas.projects_schema import Project
from schemas.users_schema import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List
from core.messages import messages
from datetime import datetime



def create(project: Project, db: Session):
    """
    Crea un proyecto 
    """
    new_project = None

    try:
        db.add(new_task)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return new_task




