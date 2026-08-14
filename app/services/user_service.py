from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.user import UserCreate


def register_user(
    db: Session,
    user_data: UserCreate,
):
    existing_email = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_email:
        raise ValueError("Email already registered")

    existing_username = get_user_by_username(
        db,
        user_data.username,
    )

    if existing_username:
        raise ValueError("Username already registered")

    hashed_password = hash_password(
        user_data.password
    )

    return create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    user = get_user_by_email(
        db,
        email,
    )

    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    return user


def login_user(
    db: Session,
    email: str,
    password: str,
):
    user = authenticate_user(
        db,
        email,
        password,
    )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }