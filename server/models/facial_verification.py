from sqlmodel import SQLModel, Field
from typing import Optional

class FacialVerification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    userId: int
    documentPhotoUrl: Optional[str]
    livePhotoUrl: Optional[str]
    verificationScore: Optional[float]
    isValid: bool = False 