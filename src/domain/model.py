from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    id: str
    name:str
    longitude: str
    latitude: str


class User(BaseModel):
    id: str
    name: str
    address: Optional[Address] = None