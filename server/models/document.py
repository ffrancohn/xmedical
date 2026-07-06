from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    userId: int
    documentType: str
    documentNumber: str
    expiryDate: Optional[date]
    frontImageUrl: Optional[str]
    backImageUrl: Optional[str]
    ocrData: Optional[str]
    isValid: bool = False 