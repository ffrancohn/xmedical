from pydantic import BaseModel
from typing import Optional
from datetime import date

class BeneficiaryBase(BaseModel):
    userId: int
    fullName: str
    documentNumber: str
    relationship: str
    birthDate: Optional[date]

class BeneficiaryCreate(BeneficiaryBase):
    pass

class BeneficiaryRead(BeneficiaryBase):
    id: int
    class Config:
        orm_mode = True 