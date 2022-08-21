from db import db_models as models
from schemas.tasks_schema import Task
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from typing import List


def create(task: Task, db: Session):
    """
    Crea una tarea 
    """
    db_task = (
        db.query(models.Task).filter(models.Task.name == task.name)
        .filter(models.Task.student_id == task.student_id).first()
    )
    if db_task is not None:
        raise HTTPException(status_code=400, detail="Item already exists")

    new_task = models.Task(
        name=task.name,
        description=task.description,
        cost=task.cost,
        student_id = task.student_id,
        project_id = task.project_id,
        tutor_id = task.tutor_id
    ) 

    db.add(new_task)
    db.commit()

    return new_task


def create_from_list(tasks: List[Task], db: Session):
    """
    Crear tareas a partir de una lista
    """
    response = {}
    successful = []
    failed = []
    for task in tasks:

        new_task = models.Task(
            name=task.name,
            description=task.description,
            cost=task.cost,
            student_id = task.student_id,
            project_id = task.project_id,
            tutor_id = task.tutor_id
        ) 
        try:
            db.add(new_task)
            db.commit()
            successful.append(new_task.name)
        except Exception as e:
            db.rollback()
            failed.append([new_task.name, str(e)])

    response['Tasks added'] = len(successful)
    response['Tasks failed'] = len(failed)
    response['successful'] = successful
    response['failed'] = failed
        
    return response
