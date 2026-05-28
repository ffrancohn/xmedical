from pydantic import BaseModel
from typing import Optional
from datetime import date

class DocumentBase(BaseModel):
    userId: int
    documentType: str
    documentNumber: str
    expiryDate: Optional[date]
    frontImageUrl: Optional[str]
    backImageUrl: Optional[str]
    ocrData: Optional[str]
    isValid: Optional[bool] = False

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int
    class Config:
        orm_mode = True 