from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    fullName: str
    profileId: int
    nationalityId: int
    phone: Optional[str]
    birthDate: Optional[date]
    gender: Optional[str]
    isActive: bool = True
    themeMode: Optional[str]
    colorTheme: Optional[str] 