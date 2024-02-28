from pydantic import BaseModel
from typing import Optional


class AddressDto(BaseModel):
    name: str
    longitude: str
    latitude: str
    user_id: str


class UserDto(BaseModel):
    name: str
