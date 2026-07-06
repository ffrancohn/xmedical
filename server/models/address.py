from sqlmodel import SQLModel, Field
from typing import Optional

class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    userId: int
    country: str
    state: str
    city: str
    zipCode: Optional[str]
    fullAddress: str
    exteriorNumber: Optional[str]
    interiorNumber: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float] 