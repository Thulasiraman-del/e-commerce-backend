from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.cart_repository import (
    add_cart_item,
    delete_cart_item,
    get_cart_by_user_id,
    get_cart_item,
    get_or_create_cart,
    update_cart_item,
)


def add_product_to_cart(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int,
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if product.stock < quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock",
        )

    cart = get_or_create_cart(db, user_id)

    return add_cart_item(
        db,
        cart.id,
        product_id,
        quantity,
    )


def get_user_cart(
    db: Session,
    user_id: int,
):
    cart = get_cart_by_user_id(db, user_id)

    if cart is None:
        return get_or_create_cart(db, user_id)

    return cart


def update_product_quantity(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int,
):
    cart = get_cart_by_user_id(db, user_id)

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Cart not found",
        )

    item = get_cart_item(
        db,
        cart.id,
        product_id,
    )

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found",
        )

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if product.stock < quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock",
        )

    return update_cart_item(
        db,
        item,
        quantity,
    )


def remove_product_from_cart(
    db: Session,
    user_id: int,
    product_id: int,
):
    cart = get_cart_by_user_id(db, user_id)

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Cart not found",
        )

    item = get_cart_item(
        db,
        cart.id,
        product_id,
    )

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found",
        )

    delete_cart_item(db, item)