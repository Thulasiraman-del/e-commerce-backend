from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(
    db: Session,
    product_data: ProductCreate,
) -> Product:

    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        image_url=product_data.image_url,
        category_id=product_data.category_id,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:

    return db.get(Product, product_id)


def get_products(
    db: Session,
) -> list[Product]:

    statement = select(Product).order_by(Product.id)

    return list(db.execute(statement).scalars().all())


def get_products_by_category(
    db: Session,
    category_id: int,
) -> list[Product]:

    statement = (
        select(Product)
        .where(Product.category_id == category_id)
        .order_by(Product.id)
    )

    return list(db.execute(statement).scalars().all())


def update_product(
    db: Session,
    product: Product,
    product_data: ProductUpdate,
) -> Product:

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product,
) -> None:

    db.delete(product)
    db.commit()