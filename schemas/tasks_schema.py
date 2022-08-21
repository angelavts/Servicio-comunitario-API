from pydantic import BaseModel
from typing import List
from datetime import datetime

# crear una tarea
class Task(BaseModel):
    name: str 
    description: str 
    cost: int 
    student_id: int 
    project_id: int 
    tutor_id: int 

    class Config:
        orm_mode = True

    


def row_to_schema(row: list):
    new_task = Task(
        name=str(row[0]), 
        description=str(row[1]),
        cost=int(row[2]),
        student_id = int(row[3]),
        project_id = int(row[4]),
        tutor_id = int(row[5])
    )
    return new_task
        
