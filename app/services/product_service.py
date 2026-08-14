from sqlalchemy.orm import Session

from app.repositories import category_repository
from app.repositories import product_repository
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(
    db: Session,
    product_data: ProductCreate,
):
    category = category_repository.get_category_by_id(
        db,
        product_data.category_id,
    )

    if not category:
        raise ValueError("Category not found")

    return product_repository.create_product(
        db,
        product_data,
    )


def get_product(
    db: Session,
    product_id: int,
):
    product = product_repository.get_product_by_id(
        db,
        product_id,
    )

    if not product:
        raise ValueError("Product not found")

    return product


def get_products(db: Session):
    return product_repository.get_products(db)


def get_products_by_category(
    db: Session,
    category_id: int,
):
    category = category_repository.get_category_by_id(
        db,
        category_id,
    )

    if not category:
        raise ValueError("Category not found")

    return product_repository.get_products_by_category(
        db,
        category_id,
    )


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
):
    product = get_product(db, product_id)

    if product_data.category_id is not None:
        category = category_repository.get_category_by_id(
            db,
            product_data.category_id,
        )

        if not category:
            raise ValueError("Category not found")

    return product_repository.update_product(
        db,
        product,
        product_data,
    )


def delete_product(
    db: Session,
    product_id: int,
):
    product = get_product(db, product_id)

    product_repository.delete_product(
        db,
        product,
    )