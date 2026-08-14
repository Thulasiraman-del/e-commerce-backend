
from sqlalchemy.orm import Session

from app.models.address import Address


def create_address(
    db: Session,
    user_id: int,
    address_data,
):
    address = Address(
        user_id=user_id,
        address_line=address_data.address_line,
        city=address_data.city,
        state=address_data.state,
        postal_code=address_data.postal_code,
        country=address_data.country,
    )

    db.add(address)
    db.commit()
    db.refresh(address)

    return address


def get_addresses_by_user(
    db: Session,
    user_id: int,
):
    return (
        db.query(Address)
        .filter(Address.user_id == user_id)
        .all()
    )


def get_address_by_id(
    db: Session,
    address_id: int,
    user_id: int,
):
    return (
        db.query(Address)
        .filter(
            Address.id == address_id,
            Address.user_id == user_id,
        )
        .first()
    )


def delete_address(
    db: Session,
    address: Address,
):
    db.delete(address)
    db.commit()
def update_address(
    db: Session,
    address: Address,
    address_data,
):
    address.address_line = address_data.address_line
    address.city = address_data.city
    address.state = address_data.state
    address.postal_code = address_data.postal_code
    address.country = address_data.country

    db.commit()
    db.refresh(address)

    return address