from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.address import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)
from app.services.address_service import (
    create_user_address,
    get_user_addresses,
    get_user_address,
    update_user_address,
    delete_user_address,
)


router = APIRouter(
    prefix="/api/addresses",
    tags=["Addresses"],
)


@router.post(
    "/",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_user_address(
        db=db,
        user_id=current_user.id,
        address_data=address_data,
    )


@router.get(
    "/",
    response_model=list[AddressResponse],
)
def get_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_addresses(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_address(
        db=db,
        user_id=current_user.id,
        address_id=address_id,
    )


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK,
)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_user_address(
        db=db,
        user_id=current_user.id,
        address_id=address_id,
        address_data=address_data,
    )


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_user_address(
        db=db,
        user_id=current_user.id,
        address_id=address_id,
    )