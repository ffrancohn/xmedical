from pydantic import BaseModel
from typing import Optional

class UserProfileBase(BaseModel):
    name: str
    description: Optional[str]
    permissions: Optional[str]

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileRead(UserProfileBase):
    id: int
    class Config:
        orm_mode = True 