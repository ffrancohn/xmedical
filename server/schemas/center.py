from pydantic import BaseModel
from typing import Optional

class CenterBase(BaseModel):
    code: str
    centerType: str
    name: str
    address: str
    phones: Optional[str]

class CenterCreate(CenterBase):
    pass

class CenterRead(CenterBase):
    id: int
    class Config:
        orm_mode = True 