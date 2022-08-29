from db import db_models as models
from schemas.tasks_schema import Task
from schemas.users_schema import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List
from core.messages import messages
from datetime import datetime


def get_user_from_identification(identification: str, error_message: str, db: Session):
    # buscar el id del estudiante
    db_user =  db.query(models.User).filter(models.User.identification == identification).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail=messages[error_message])
    
    return db_user



def create(task: Task, db: Session):
    """
    Crea una tarea 
    """

    # buscar el id del estudiante
    db_student = get_user_from_identification(task.student_identification, 'student_not_exists', db)

    # buscar si existe la tarea
    db_task = (
        db.query(models.Task).filter(models.Task.name == task.name)
        .filter(models.Task.student_id == db_student.id).first()
    )
    if db_task is not None:
        raise HTTPException(status_code=400, detail=messages['task_exists'])


    # buscar el id del tutor
    db_tutor = get_user_from_identification(task.tutor_identification, 'tutor_not_exists', db)

    new_task = models.Task(
        name=task.name,
        description=task.description,
        cost=task.cost,
        student_id = db_student.id,
        project_id = task.project_id,
        tutor_id = db_tutor.id
    ) 

    try:
        db.add(new_task)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return new_task


def get_tasks_from_student(project_id: int, student_identification: str, db: Session):

    # buscar el id del estudiante
    db_student = get_user_from_identification(student_identification, 'student_not_exists', db)

    db_tasks = (db.query(
                    models.Task.id, 
                    models.Task.name, 
                    models.Task.description,
                    models.Task.cost,
                    models.Task.date_start,
                    models.Task.date_end,
                    models.Task.status,
                    models.User.first_name.label('Tutor'))
                    .join(models.User, models.User.id == models.Task.tutor_id)
                    .filter(models.Task.student_id == db_student.id)
                    .all())
    return db_tasks


def update_task_status(task_id: int, status: str, db: Session):
    """
    Actualizar el status de una tarea 
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=400, detail=messages['task_not_exists'])

    # cambiar status de la tarea
    db_task.status = status
    # si la tarea está completada
    if status == 'Completada':
        # agregar fecha de finalización
        db_task.date_end = datetime.now()
    try:
        db.add(db_task)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_task



