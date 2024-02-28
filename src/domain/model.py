from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class Address(BaseModel):
    id: str
    name: str
    longitude: Decimal
    latitude: Decimal


class User(BaseModel):
    id: str
    name: str
    address: Optional[Address] = None
