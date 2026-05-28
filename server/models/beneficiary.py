from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Beneficiary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    userId: int
    fullName: str
    documentNumber: str
    relationship: str
    birthDate: Optional[date] 