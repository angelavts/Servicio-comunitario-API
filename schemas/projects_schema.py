from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# crear un proyecto
class Project(BaseModel):
    name: str 
    description: str 
    date_start: str 
    career: str
    coordinator_identification: str     
    coordinator_first_name: str 
    coordinator_last_name: str
    coordinator_career: Optional[str] = None 
    coordinator_email: Optional[str] = None
    coordinator_phone: Optional[str] = None

    class Config:
        orm_mode = True

def row_to_schema(row: list):
    new_user = Project(
            name=str(row[0]), 
            description=str(row[1]), 
            date_start=str(row[2]),            
            career=str(row[3]),
            coordinator_identification=str(row[4]),
            coordinator_first_name=str(row[5]),
            coordinator_last_name=str(row[6]),
            coordinator_career=str(row[7]),
            coordinator_email=str(row[8]),
            coordinator_phone=str(row[9])
    )
    return new_user
        
