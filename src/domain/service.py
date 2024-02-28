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
from src.domain.dto import AddressDto, UserDto
import geocoder


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
        address_dto = AddressDto(
            name=address_request.name,
            longitude=longitude,
            latitude=latitude,
            user_id=user.id,
        )

        user.address = store.address.create_address(address_dto)

    return user


def _get_coordinates(value: str) -> tuple[str, str]:
    coordinates = geocoder.osm(value)
    if not coordinates.osm:
        raise AddressNotFound("Unable to locate address name")

    return str(coordinates.osm["x"]), str(coordinates.osm["y"])


def update_address(ports: Ports, request: UpdateAddressRequest) -> Address:
    with ports.mutable_store() as store:
        longitude, latitude = _get_coordinates(request.name)
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

    return
