from pydantic import BaseModel
from typing import List
from datetime import datetime

# crear un proyecto
class Project(BaseModel):
    name: str 
    description: str 
    date_start: datetime 
    career: str
    coordinator_identification: str     
    coordinator_first_name: str 
    coordinator_last_name: str
    coordinator_career: str 

    class Config:
        orm_mode = True
        
