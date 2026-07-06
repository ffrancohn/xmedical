from sqlmodel import SQLModel, Field
from typing import Optional

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]
    permissions: Optional[str]  # Puede ser un JSON o string serializado 