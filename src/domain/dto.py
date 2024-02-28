from pydantic import BaseModel, field_validator

from typing import Optional
from decimal import Decimal

class AddressDto(BaseModel):
    name: str
    longitude: Decimal
    latitude: Decimal

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


class UpdateAddressDto(AddressDto):
    id: str


class CreateAddressDto(AddressDto):
    user_id: str


class UserDto(BaseModel):
    name: str
