from sqlalchemy.orm import Session

from app.repositories import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(
    db: Session,
    category_data: CategoryCreate,
):
    existing_category = category_repository.get_category_by_name(
        db,
        category_data.name,
    )

    if existing_category:
        raise ValueError("Category already exists")

    return category_repository.create_category(
        db,
        category_data,
    )


def get_category(
    db: Session,
    category_id: int,
):
    category = category_repository.get_category_by_id(
        db,
        category_id,
    )

    if not category:
        raise ValueError("Category not found")

    return category


def get_categories(db: Session):
    return category_repository.get_categories(db)


def update_category(
    db: Session,
    category_id: int,
    category_data: CategoryUpdate,
):
    category = get_category(db, category_id)

    return category_repository.update_category(
        db,
        category,
        category_data,
    )


def delete_category(
    db: Session,
    category_id: int,
):
    category = get_category(db, category_id)

    category_repository.delete_category(
        db,
        category,
    )