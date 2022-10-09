from db import db_models as models
from schemas.tasks_schema import Task
from schemas.users_schema import User
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from fastapi import status, HTTPException
from typing import List
from core.messages import messages
from datetime import datetime
from db.enums import TaskStatusEnum, UserStatusEnum
import crud

# ------------------------------------------ TOOLS -------------------------------------------




# ------------------------------------------ POST ------------------------------------

def create(task: Task, db: Session):
    """
    Crea una tarea 
    """

    # buscar el id del estudiante
    db_student = crud.users.get_user_by_identification(task.student_identification, db)

    if db_student is None:
        raise HTTPException(status_code=400, detail=messages['student_not_exists'])

    # buscar si existe la tarea
    db_task = (
        db.query(models.Task).filter(models.Task.name == task.name)
        .filter(models.Task.student_id == db_student.id).first()
    )
    if db_task is not None:
        raise HTTPException(status_code=400, detail=messages['task_exists'])

    # buscar si existe el proyecto
    db_project = crud.projects.get_project_by_id(task.project_id, 'project_not_exists', db)

    # buscar si el proyecto de la tarea coincide con el proyecto
    # que tiene el estudiante activo
    filters = [models.ProjectStudent.student_id == db_student.id, models.ProjectStudent.active == True]
    db_project_active = db.query(models.ProjectStudent).filter(*filters).first()

    if db_project_active == None or db_project_active.project_id != task.project_id:
        raise HTTPException(status_code=400, detail=messages['incorrect_project'])

    # buscar el id del tutor
    db_tutor = crud.users.get_user_by_identification(task.tutor_identification, db)

    new_task = models.Task(
        name=task.name,
        description=task.description,
        cost=task.cost,
        student_id = db_student.id,
        project_id = task.project_id,
        tutor_id = db_tutor.id if db_tutor != None else None
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

    if db_task.status != status:
        hours = 0        
        # si la tarea está completada
        if status == TaskStatusEnum.Completed:
            # agregar fecha de finalización
            db_task.date_end = datetime.now()
            # sumar las horas
            crud.users.update_hours(db_task.student_id, db_task.cost, db)
        elif db_task.status == TaskStatusEnum.Completed:
            # si la tarea estaba completada
            # quitar fecha de finalización
            db_task.date_end = None
            # restar las horas
            crud.users.update_hours(db_task.student_id, -db_task.cost)

        # cambiar status de la tarea
        db_task.status = status
        # guardar cambios en la db
        try:
            db.add(db_task)
            db.commit()        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=messages['internal_error'])
    return db_task

# ------------------------------------------ GET ------------------------------------



def get_tasks_by_student(student_identification: str, db: Session):

    # buscar el id del estudiante
    db_student = crud.users.get_user_by_identification(student_identification, db)

    if db_student == None:
        raise HTTPException(status_code=500, detail=messages['student_not_exists'])


    tutor_alias = aliased(models.User, name='tutor')
    # buscar el proyecto que tiene activo el estudiante
    project = crud.projects.get_active_project_by_student_id(db_student.id, db)

    db_tasks = []
    if project != None:

        db_tasks = (db.query(
                        models.Task.id, 
                        models.Task.name, 
                        models.Task.description,  
                        tutor_alias.identification.label('tutor_indentification'), 
                        tutor_alias.fullname.label('tutor_name'),                  
                        models.Task.date_start,
                        models.Task.date_end,
                        models.Task.cost,
                        models.Task.status
                        )
                        .outerjoin(tutor_alias, tutor_alias.id == models.Task.tutor_id)
                        .filter(models.Task.student_id == db_student.id)
                        .filter(models.Task.project_id == project.id)
                        .all())
    return db_tasks

def get_tasks_by_project(project_id: int, db: Session):
    """
        Filtra las tareas de un proyecto incluyendo el estudiante asignado, teniendo
        en cuenta que el estudiante debe estar activo y debe tener ese proyecto activo    
    """

    # buscar el id del proyecto
    db_project = crud.projects.get_project_by_id(project_id, 'project_not_exists', db)

    user_alias = aliased(models.User, name='student')
    tutor_alias = aliased(models.User, name='tutor')

    db_tasks = (db.query(
                    models.Task.id, 
                    models.Task.name, 
                    models.Task.description, 
                    user_alias.identification, 
                    user_alias.fullname,                  
                    models.Task.date_start,
                    models.Task.date_end,
                    models.Task.cost,
                    models.Task.status 
                    )
                    .filter(models.Task.project_id == db_project.id)
                    .join(user_alias, user_alias.id == models.Task.student_id)
                    .filter(user_alias.status == UserStatusEnum.Active)
                    .join(models.ProjectStudent, user_alias.id == models.ProjectStudent.student_id)
                    .filter(models.ProjectStudent.active)   
                    .outerjoin(tutor_alias, tutor_alias.id == models.Task.tutor_id)                 
                    .all())
    return db_tasks


def get_tasks_by_tutor(tutor_identification: str, db: Session):
    """
        Filtra las tareas de un tutor incluyendo el estudiante asignado, teniendo
        en cuenta que el estudiante debe estar activo y debe tener activo
        el proyecto que corresponde a la tarea   
    """

    # buscar el id del tutor
    db_tutor = crud.users.get_user_by_identification(tutor_identification, db)

    if db_tutor is None:
        raise HTTPException(status_code=400, detail=messages['tutor_not_exists'])

    student_alias = aliased(models.User, name='student')
    project_alias = aliased(models.Project, name='project')

    db_tasks = (db.query(
                    models.Task.id, 
                    models.Task.name, 
                    models.Task.description,
                    student_alias.identification.label('student_indentification'),
                    student_alias.fullname.label('student_name'),
                    project_alias.id.label('project_id'),
                    project_alias.name.label('project_name'), 
                    models.Task.cost,
                    models.Task.date_start,
                    models.Task.date_end,
                    models.Task.status                                    
                    )
                    .filter(models.Task.tutor_id == db_tutor.id)
                    .join(student_alias, student_alias.id == models.Task.student_id)
                    .filter(student_alias.status == UserStatusEnum.Active)
                    .join(models.ProjectStudent, student_alias.id == models.ProjectStudent.student_id)
                    .filter(models.ProjectStudent.active)      
                    .join(project_alias, project_alias.id == models.Task.project_id)              
                    .all())
    return db_tasks





