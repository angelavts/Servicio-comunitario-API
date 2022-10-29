from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserIdentification(BaseModel):
    identification: str 

    class Config:
        orm_mode = True

class IdList(BaseModel):
    id_list: List[int] 

    class Config:
        orm_mode = True



class UserUpdate(BaseModel):
    identification: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    career: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    project_id: Optional[int] = None

    class Config:
        orm_mode = True

class ProjectUpdate(BaseModel):

    name: Optional[str] = None
    description: Optional[str] = None
    date_end: Optional[datetime] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True