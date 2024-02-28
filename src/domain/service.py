from src.contexts.address import Ports

from .exceptions import RowNotFound, AddressNotFound

from .model import User, Address

from .request import (
    UserRequest,
    UserResponse,
    UpdateAddressRequest,
    AddressResponse,
    UpdateAddressRequestBody,
    PerimeterRequest,
)

from src.domain.dto import (
    AddressDto,
    UserDto,
    CreateAddressDto,
    UpdateAddressDto,
    PerimeterDto,
)

import geocoder

from geopy import distance
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
            name=request.name,
            longitude=longitude,
            latitude=latitude,
            id=request.id,
        )

        address = store.address.update_address(address_dto)

    return address


def delete_address(ports: Ports, address_id: str) -> None:
    with ports.mutable_store() as store:
        address = store.address.delete_address(address_id)


def get_addresses_within_perimeter(
    ports: Ports, request: PerimeterRequest
) -> list[Address]:
    max_latitude = request.latitude + request.distance
    min_latitude = request.latitude - request.distance

    max_longitude = request.longitude + request.distance
    min_longitude = request.longitude - request.distance

    perimeter = PerimeterDto(
        max_latitude=max_latitude,
        min_latitude=min_latitude,
        max_longitude=max_longitude,
        min_longitude=min_longitude,
    )

    with ports.store() as store:
        addresses = store.address.get_all_addresses_within_perimeter(perimeter)

    return addresses


def get_addresses_within_kilometers(
    ports: Ports, request: PerimeterRequest
) -> list[Address]:
    with ports.store() as store:
        addresses: list[Address] = store.address.get_all_addresses()

    addresses_within_distance = _filter_within_distance(
        addresses=addresses, request=request
    )

    return addresses_within_distance


def _filter_within_distance(
    addresses: list[Address], request: PerimeterRequest
) -> list[Address]:
    coordinate = (request.latitude, request.longitude)

    new_addresses = []
    for address in addresses:
        existing_coordinate = (address.latitude, address.longitude)
        distance_from_coordinate = distance.distance(
            coordinate, existing_coordinate
        ).kilometers
        within_distance = request.distance >= distance_from_coordinate
        if within_distance:
            new_addresses.append(address)

    return new_addresses
