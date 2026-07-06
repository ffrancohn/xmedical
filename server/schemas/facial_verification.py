from pydantic import BaseModel
from typing import Optional

class FacialVerificationBase(BaseModel):
    userId: int
    documentPhotoUrl: Optional[str]
    livePhotoUrl: Optional[str]
    verificationScore: Optional[float]
    isValid: Optional[bool] = False

class FacialVerificationCreate(FacialVerificationBase):
    pass

class FacialVerificationRead(FacialVerificationBase):
    id: int
    class Config:
        orm_mode = True 