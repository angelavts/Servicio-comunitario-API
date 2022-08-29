from pydantic import BaseModel
from typing import List
from datetime import datetime

# crear una tarea
class Task(BaseModel):
    name: str 
    description: str 
    cost: int 
    student_identification: str     
    tutor_identification: str 
    project_id: int 

    class Config:
        orm_mode = True
        
