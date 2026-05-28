from pydantic import BaseModel
from typing import Optional

class FeedbackBase(BaseModel):
    userId: int
    type: str
    subject: str
    message: str
    priority: str
    status: str
    response: Optional[str]
    respondedBy: Optional[int]

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackRead(FeedbackBase):
    id: int
    class Config:
        orm_mode = True 