from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.address_repository import (
    create_address,
    get_addresses_by_user,
    get_address_by_id,
    update_address,
    delete_address,
)


def create_user_address(
    db: Session,
    user_id: int,
    address_data,
):
    return create_address(
        db=db,
        user_id=user_id,
        address_data=address_data,
    )


def get_user_addresses(
    db: Session,
    user_id: int,
):
    return get_addresses_by_user(
        db=db,
        user_id=user_id,
    )


def get_user_address(
    db: Session,
    user_id: int,
    address_id: int,
):
    address = get_address_by_id(
        db=db,
        address_id=address_id,
        user_id=user_id,
    )

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    return address


def update_user_address(
    db: Session,
    user_id: int,
    address_id: int,
    address_data,
):
    address = get_user_address(
        db=db,
        user_id=user_id,
        address_id=address_id,
    )

    return update_address(
        db=db,
        address=address,
        address_data=address_data,
    )


def delete_user_address(
    db: Session,
    user_id: int,
    address_id: int,
):
    address = get_user_address(
        db=db,
        user_id=user_id,
        address_id=address_id,
    )

    delete_address(
        db=db,
        address=address,
    )

    return {
        "message": "Address deleted successfully"
    }