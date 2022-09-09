from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserIdentification(BaseModel):
    identification: str 

    class Config:
        orm_mode = True

class IdList(BaseModel):
    id_list: List[int] 

    class Config:
        orm_mode = True