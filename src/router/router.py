from fastapi import Depends, FastAPI, Path, status, HTTPException, Request, Query

from src.domain.request import (
    UserRequest,
    UserResponse,
    UpdateAddressRequest,
    AddressResponse,
    PerimeterRequest,
    UpdateAddressRequestBody,
)

from src.domain import service

from src.contexts.address import Ports

from typing import Optional, Annotated

from src.domain.exceptions import RowNotFound, AddressNotFound

from fastapi.responses import JSONResponse


app = FastAPI()


@app.exception_handler(RowNotFound)
async def row_not_found_handler(request: Request, exc: RowNotFound) -> None:

    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(AddressNotFound)
async def row_not_found_handler(request: Request, exc: AddressNotFound) -> None:

    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.get("/")
async def health_check():
    return {"message": "Hello World"}


@app.get("/user", response_model=Optional[UserResponse], status_code=status.HTTP_200_OK)
async def get_user(id: str) -> Optional[UserResponse]:
    ports = Ports()
    user = service.get_user_by_id(ports, id)

    return UserResponse.model_validate(user.model_dump())


@app.post(
    "/user", response_model=Optional[UserResponse], status_code=status.HTTP_201_CREATED
)
async def create_user(request: UserRequest) -> Optional[UserResponse]:
    ports = Ports()

    user = service.create_user(ports, request)
    return UserResponse.model_validate(user.model_dump())


@app.put(
    "/address/{address_id}",
    response_model=Optional[AddressResponse],
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_address(
    address_id: Annotated[str, Path], request: UpdateAddressRequestBody
) -> Optional[AddressResponse]:
    ports = Ports()

    update_request = UpdateAddressRequest(id=address_id, name=request.name)

    address = service.update_address(ports, update_request)

    return AddressResponse.model_validate(address.model_dump())


@app.delete(
    "/address/{address_id}",
    response_model=Optional[AddressResponse],
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_address(
    address_id: Annotated[str, Path],
) -> JSONResponse:
    ports = Ports()

    address = service.delete_address(ports, address_id)

    return JSONResponse(
        status_code=202, content={"message": "Delete request successfully"}
    )


@app.get(
    "/users",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    description="Get the available users based on the coordinates given within the given distance perimeter in km",
)
async def get_users_within_kilometers(
    request: PerimeterRequest = Depends(),
) -> list[AddressResponse]:
    ports = Ports()

    users = service.get_users_within_kilometers(ports, request)

    response = [UserResponse.model_validate(user.model_dump()) for user in users]

    return response
