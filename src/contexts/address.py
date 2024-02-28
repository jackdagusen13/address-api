import contextlib
from typing import Generator
from src.adapter.schema import get_session_maker
from sqlalchemy.orm import Session
from dataclasses import dataclass
from src.adapter.address_adapter import AddressAdapter
from src.domain.ports.address import (
    UserQuery,
    AddressQuery,
    UserMutation,
    AddressMutation,
)
from src.domain.ports.address import Ports as PortsInterface


@dataclass
class Store:
    session: Session

    @property
    def user(self) -> UserQuery:
        return AddressAdapter(self.session)

    @property
    def address(self) -> AddressQuery:
        return AddressAdapter(self.session)


@dataclass
class MutableStore:
    session: Session

    @property
    def user(self) -> UserMutation:
        return AddressAdapter(self.session)

    @property
    def address(self) -> AddressMutation:
        return AddressAdapter(self.session)


class Ports(PortsInterface):
    def __init__(self) -> None:
        self._session_maker = get_session_maker()

    @contextlib.contextmanager
    def store(self) -> Generator[Store, None, None]:
        with self._session_maker.begin() as session:
            yield Store(session=session)

    @contextlib.contextmanager
    def mutable_store(self) -> Generator[MutableStore, None, None]:
        with self._session_maker.begin() as session:
            yield MutableStore(session=session)
