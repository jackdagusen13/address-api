from typing import Protocol, Optional, Generator
from src.domain.dto import (
    AddressDto,
    UserDto,
    UpdateAddressDto,
    CreateAddressDto,
    PerimeterDto,
)
from src.domain.model import Address, User
import contextlib
from decimal import Decimal


class UserQuery(Protocol):
    def get_user(user_id: str) -> Optional[User]:
        """Get a user"""


class UserMutation(UserQuery, Protocol):
    def create_user(self, user: UserDto) -> Optional[User]:
        """Create a user"""


class AddressQuery(Protocol):
    def get_address_by_user_id(self, user_id: str) -> Address:
        """Get an address by user_id"""

    def get_address_by_id(self, id: str) -> Address:
        """Get an address by id"""

    def get_all_addresses_within_perimeter(
        self, perimeter: PerimeterDto
    ) -> list[Address]:
        """Get address within a perimeter in longitude/latitude"""

    def get_all_users(self) -> list[User]:
        """Get all users"""


class AddressMutation(AddressQuery, Protocol):
    def create_address(self, address: CreateAddressDto) -> Address:
        """Create an address"""

    def update_address(self, address: UpdateAddressDto) -> Address:
        """Update an address"""

    def delete_address(self, address_id: str) -> None:
        """delete an address"""


class Store(Protocol):
    user: UserQuery
    address: AddressQuery


class MutableStore(Protocol):
    user: UserMutation
    address: AddressMutation


class Ports(Protocol):
    @contextlib.contextmanager
    def store(self) -> Generator[Store, None, None]:
        """Read only transactions"""

    @contextlib.contextmanager
    def mutable_store(self) -> Generator[MutableStore, None, None]:
        """Read and mutation transactions"""
