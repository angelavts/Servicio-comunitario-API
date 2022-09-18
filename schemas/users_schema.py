from pydantic import BaseModel
from typing import List
from datetime import datetime

# crear un usuario
class User(BaseModel):
    identification: str
    first_name: str
    last_name: str
    career: str
    email: str
    phone: str

    class Config:
        orm_mode = True



def row_to_schema(row: list):
    new_user = User(
        identification=str(row[0]), 
        first_name=str(row[1]), 
        last_name=str(row[2]),            
        career=str(row[3]),
        email=str(row[4]),
        phone=str(row[5]),
    )
    return new_user