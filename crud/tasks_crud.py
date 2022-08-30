from db import db_models as models
from schemas.tasks_schema import Task
from schemas.users_schema import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List
from core.messages import messages
from datetime import datetime
from db.enums import TaskStatusEnum, UserStatusEnum




# ------------------------------------------ POST ------------------------------------

def create(task: Task, db: Session):
    """
    Crea una tarea 
    """

    # buscar el id del estudiante
    db_student = get_user_by_identification(task.student_identification, 'student_not_exists', db)

    # buscar si existe la tarea
    db_task = (
        db.query(models.Task).filter(models.Task.name == task.name)
        .filter(models.Task.student_id == db_student.id).first()
    )
    if db_task is not None:
        raise HTTPException(status_code=400, detail=messages['task_exists'])


    # buscar el id del tutor
    db_tutor = get_user_by_identification(task.tutor_identification, 'tutor_not_exists', db)

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

# ------------------------------------------ UPDATE ------------------------------------

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
    if status == TaskStatusEnum.Completed:
        # agregar fecha de finalización
        db_task.date_end = datetime.now()
    try:
        db.add(db_task)
        db.commit()        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_task

# ------------------------------------------ GET ------------------------------------

def get_user_by_identification(identification: str, error_message: str, db: Session):
    # buscar el id del estudiante
    db_user =  db.query(models.User).filter(models.User.identification == identification).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail=messages[error_message])
    
    return db_user

def get_project_by_id(project_id: str, error_message: str, db: Session):
    # buscar el id del estudiante
    db_user =  db.query(models.Project).filter(models.Project.id == project_id).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail=messages[error_message])
    
    return db_user

def get_tasks_by_student(project_id: int, student_identification: str, db: Session):

    # buscar el id del estudiante
    db_student = get_user_by_identification(student_identification, 'student_not_exists', db)

    db_tasks = (db.query(
                    models.Task.id, 
                    models.Task.name, 
                    models.Task.description,
                    models.Task.cost,
                    models.Task.date_start,
                    models.Task.date_end,
                    models.Task.status,
                    models.User.first_name.label('tutor_first_name'),
                    models.User.first_name.label('tutor_last_name'),
                    )
                    .join(models.User, models.User.id == models.Task.tutor_id)
                    .filter(models.Task.student_id == db_student.id)
                    .all())
    return db_tasks

def get_tasks_by_project(project_id: int, db: Session):
    """
        Filtra las tareas de un proyecto incluyendo el estudiante asignado, teniendo
        en cuenta que el estudiante debe estar activo y debe tener ese proyecto activo    
    """

    # buscar el id del proyecto
    db_project = get_project_by_id(project_id, 'project_not_exists', db)

    db_tasks = (db.query(
                    models.Task.id, 
                    models.Task.name, 
                    models.Task.description,
                    models.Task.cost,
                    models.Task.date_start,
                    models.Task.date_end,
                    models.Task.status,
                    models.Task.student_id,
                    models.Task.tutor_id,
                    models.User.first_name.label('student_first_name'),
                    models.User.last_name.label('student_last_name')
                    
                    )
                    .filter(models.Task.project_id == db_project.id)
                    .join(models.User, models.User.id == models.Task.student_id)
                    .filter(models.User.status == UserStatusEnum.Active)
                    .join(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                    .filter(models.ProjectStudent.active)                    
                    .all())
    return db_tasks


def get_tasks_by_tutor(tutor_identification: str, db: Session):
    """
        Filtra las tareas de un tutor incluyendo el estudiante asignado, teniendo
        en cuenta que el estudiante debe estar activo y debe tener activo
        el proyecto que corresponde a la tarea   
    """

    # buscar el id del tutor
    db_tutor = get_user_by_identification(tutor_identification, 'tutor_not_exists', db)

    db_tasks = (db.query(
                    models.Task.id, 
                    models.Task.name, 
                    models.Task.description,
                    models.Task.cost,
                    models.Task.date_start,
                    models.Task.date_end,
                    models.Task.status,
                    models.Task.student_id,
                    models.User.first_name.label('student_first_name'),
                    models.User.last_name.label('student_last_name'),
                    models.Task.project_id,
                    models.Project.name.label('project_name')                 
                    )
                    .filter(models.Task.tutor_id == db_tutor.id)
                    .join(models.User, models.User.id == models.Task.student_id)
                    .filter(models.User.status == UserStatusEnum.Active)
                    .join(models.ProjectStudent, models.User.id == models.ProjectStudent.student_id)
                    .filter(models.ProjectStudent.active)      
                    .join(models.Project, models.Project.id == models.Task.project_id)              
                    .all())
    return db_tasks





