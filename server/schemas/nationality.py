from pydantic import BaseModel
from typing import Optional

class NationalityBase(BaseModel):
    code: str
    name: str

class NationalityCreate(NationalityBase):
    pass

class NationalityRead(NationalityBase):
    id: int
    class Config:
        orm_mode = True 