from sqlalchemy import (
    create_engine,
    String,
    Column,
    Text,
    MetaData,
    ForeignKey,
    inspect,
    Numeric,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import uuid


class Base(DeclarativeBase):
    """Base Model for Rows"""


class UserRow(Base):
    __tablename__ = "user"
    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)

    def dict(self) -> dict:
        return {"id": self.id, "name": self.name}


class AddressRow(Base):
    __tablename__ = "address"
    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    longitude = Column(Numeric, nullable=True)
    latitude = Column(Numeric, nullable=True)
    user_id = Column(
        String,
        ForeignKey(
            UserRow.id,
            name="user_id",
        ),
        nullable=False,
    )

    def dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "longitude": self.longitude,
            "latitude": self.latitude,
        }


engine = create_engine(url="sqlite:///places.db", echo=True)


def get_session_maker() -> sessionmaker:
    insp = inspect(engine)
    return sessionmaker(bind=engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
