from sqlmodel import SQLModel, Field
from typing import Optional

class Nationality(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    name: str 