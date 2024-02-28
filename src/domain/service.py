from src.contexts.address import Ports

from .exceptions import RowNotFound, AddressNotFound

from .model import User, Address

from .request import (
    UserRequest,
    UserResponse,
    UpdateAddressRequest,
    AddressResponse,
    UpdateAddressRequestBody,
)

from src.domain.dto import AddressDto, UserDto, CreateAddressDto, UpdateAddressDto

import geocoder

from decimal import Decimal


def get_user_by_id(ports: Ports, id: str) -> User:
    with ports.store() as store:
        user = store.user.get_user(id)
        try:
            address = store.address.get_address_by_user_id(id)
        except RowNotFound:
            return user

        user.address = address

    return user


def create_user(ports: Ports, request: UserRequest) -> User:
    user_dto = UserDto(name=request.name)
    with ports.mutable_store() as store:

        user: User = store.user.create_user(user_dto)

        address_request = request.address

        if not address_request:
            return user

        longitude, latitude = _get_coordinates(address_request.name)

        address_dto = CreateAddressDto(
            name=address_request.name,
            longitude=longitude,
            latitude=latitude,
            user_id=user.id,
        )

        user.address = store.address.create_address(address_dto)

    return user


def _get_coordinates(value: str) -> tuple[Decimal, Decimal]:
    coordinates = geocoder.osm(value)
    if not coordinates.osm:
        raise AddressNotFound("Unable to locate address name")

    return Decimal(str(coordinates.osm["x"])), Decimal(str(coordinates.osm["y"]))


def update_address(ports: Ports, request: UpdateAddressRequest) -> Address:
    with ports.mutable_store() as store:
        longitude, latitude = _get_coordinates(request.name)

        address_dto = UpdateAddressDto(
            name=address_request.name,
            longitude=longitude,
            latitude=latitude,
            id=request.id,
        )

        address = store.address.update_address(
            request.id,
            request.name,
            longitude,
            latitude,
        )

    return address


def delete_address(ports: Ports, address_id: str) -> None:
    with ports.mutable_store() as store:
        address = store.address.delete_address(address_id)


def get_addresses_within_perimeter(ports: Ports, distance: Decimal) -> list[Address]:
    with ports.store() as store:
        store.address.get_all_addresses_with_parameter
