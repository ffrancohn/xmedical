from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
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

class AddressCreate(AddressBase):
    pass

class AddressRead(AddressBase):
    id: int
    class Config:
        orm_mode = True 