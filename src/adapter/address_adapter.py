from sqlalchemy.orm import Session, sessionmaker

from src.domain.ports.address import AddressMutation, UserMutation
from src.domain.dto import (
    AddressDto,
    UserDto,
    CreateAddressDto,
    UpdateAddressDto,
    PerimeterDto,
)
from src.domain.model import Address, User
from src.domain.exceptions import RowNotFound
from src.adapter.schema import UserRow, AddressRow
from typing import Optional
from sqlalchemy import select, insert, update, delete
from src.adapter.schema import engine
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from decimal import Decimal

Session = sessionmaker(bind=engine)


local_session = Session()


class AddressAdapter(AddressMutation, UserMutation):

    def __init__(self, session: Session = local_session):
        self.session = session

    def create_user(self, user: UserDto) -> User:
        data = user.model_dump()

        data["id"] = str(uuid4())
        statement = insert(UserRow).values(data)

        self.session.execute(statement)

        return User(**data)

    def create_address(self, address: CreateAddressDto) -> Address:
        data = address.model_dump()

        data["id"] = str(uuid4())

        statement = insert(AddressRow).values(data)

        self.session.execute(statement)

        return Address(**data)

    def get_user(self, user_id: str) -> User:
        query = select(UserRow).where(UserRow.id == user_id)
        try:
            row = self.session.scalars(query).one()
        except NoResultFound:
            raise RowNotFound("No user found")

        return User(**row.dict())

    def get_address_by_user_id(self, user_id: str) -> Optional[Address]:
        query = (
            select(AddressRow)
            .join(UserRow)
            .where(
                UserRow.id == user_id,
            )
        )
        try:
            row = self.session.scalars(query).one()
        except NoResultFound:
            raise RowNotFound("No address found")

        return Address(**row.dict())

    def get_address_by_id(self, id: str) -> Optional[Address]:
        query = select(AddressRow).where(
            AddressRow.id == id,
        )
        try:
            row = self.session.scalars(query).one()
        except NoResultFound:
            raise RowNotFound("No address found")

        return Address(**row.dict())

    def update_address(self, address: UpdateAddressDto) -> Address:
        query = (
            update(AddressRow)
            .where(AddressRow.id == address.id)
            .values(
                name=address.name,
                longitude=address.longitude,
                latitude=address.latitude,
            )
            .returning(AddressRow)
        )
        try:
            row = self.session.scalars(query).one()
        except NoResultFound:
            raise RowNotFound("No address found")

        return Address(**row.dict())

    def delete_address(self, address_id: str) -> None:
        try:
            query = delete(AddressRow).where(AddressRow.id == address_id)
            self.session.execute(query)
        except NoResultFound:
            raise RowNotFound("No address found")

    def get_all_addresses_within_perimeter(
        self, perimeter: PerimeterDto
    ) -> list[Address]:
        try:
            rows = self.session.query(AddressRow).where(
                AddressRow.latitude <= perimeter.max_latitude,
                AddressRow.latitude >= perimeter.min_latitude,
                AddressRow.longitude <= perimeter.max_longitude,
                AddressRow.longitude >= perimeter.min_longitude,
            )
        except NoResultFound:
            return []

        return [Address(**row.dict()) for row in rows]

    def get_all_users(self) -> list[User]:
        try:
            rows: list[tuple[UserRow, AddressRow]] = (
                self.session.query(UserRow, AddressRow).join(AddressRow).all()
            )
        except NoResultFound:
            return []

        users = []
        for user_row, address_row in rows:
            user = User(**user_row.dict())

            user.address = Address(**address_row.dict()) if address_row else None

            users.append(user)

        return users
