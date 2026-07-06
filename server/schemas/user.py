from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    username: str
    email: EmailStr
    fullName: str
    profileId: int
    nationalityId: int
    phone: Optional[str]
    birthDate: Optional[date]
    gender: Optional[str]
    isActive: Optional[bool] = True
    themeMode: Optional[str]
    colorTheme: Optional[str]

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True 