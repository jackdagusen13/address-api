from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal


class AddressRequest(BaseModel):
    name: str


class PerimeterRequest(BaseModel):
    latitude: Decimal
    longitude: Decimal
    distance: Decimal

    @field_validator("longitude")
    def validate_longitude(cls, value: Decimal) -> Decimal:
        if value < -180 or value > 180:
            raise ValueError("Must be between -180 and 180")

        return value

    @field_validator("latitude")
    def validate_latitude(cls, value: Decimal) -> Decimal:
        if value < -90 or value > 90:
            raise ValueError("Must be between -90 and 90")

        return value


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
