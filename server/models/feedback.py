from sqlmodel import SQLModel, Field
from typing import Optional

class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    userId: int
    type: str
    subject: str
    message: str
    priority: str
    status: str
    response: Optional[str]
    respondedBy: Optional[int] 