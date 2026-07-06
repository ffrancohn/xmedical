from sqlmodel import SQLModel, Field
from typing import Optional

class Center(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    centerType: str
    name: str
    address: str
    phones: Optional[str] 