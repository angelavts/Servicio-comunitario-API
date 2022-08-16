from fastapi import APIRouter, Depends, HTTPException
from schemas.tasks_schema import Task
from db.db import get_db
from sqlalchemy.orm import Session
# crear router

api_router = APIRouter()


# crear tarea
@api_router.post('/')
def read_document(db: Session = Depends(get_db)):
    """
    read a document5
    """

    return {}