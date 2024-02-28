from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal

class AddressRequest(BaseModel):
    name: str


class AddressResponse(AddressRequest):
    id: str
    longitude: Decimal
    latitude: Decimal


class UserRequest(BaseModel):
    name: str
    address: Optional[AddressRequest] = None

    @field_validator("name")
    def must_be_full_name(cls, value: str) -> str:
        if " " not in value:
            raise ValueError("Must be a full name containing a space")

        return value.title()


class UserResponse(BaseModel):
    id: str
    name: str
    address: Optional[AddressResponse] = None


class UpdateAddressRequestBody(BaseModel):
    name: str


class UpdateAddressRequest(UpdateAddressRequestBody):
    id: str
