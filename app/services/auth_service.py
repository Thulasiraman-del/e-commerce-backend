from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)
from app.schemas.user import UserCreate


def register_user(
    db: Session,
    user_data: UserCreate,
):
    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:
        raise ValueError(
            "Email already registered"
        )

    hashed_password = hash_password(
        user_data.password
    )

    user = create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    return user


def login_user(
    db: Session,
    email: str,
    password: str,
):
    user = get_user_by_email(
        db,
        email,
    )

    if not user:
        raise ValueError(
            "Invalid email or password"
        )

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise ValueError(
            "Invalid email or password"
        )

    if not user.is_active:
        raise ValueError(
            "User account is inactive"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }