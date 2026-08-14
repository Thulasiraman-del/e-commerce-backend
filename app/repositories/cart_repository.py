from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem


def get_cart_by_user_id(db: Session, user_id: int):
    return (
        db.query(Cart)
        .filter(Cart.user_id == user_id)
        .first()
    )


def create_cart(db: Session, user_id: int):
    cart = Cart(user_id=user_id)

    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart


def get_or_create_cart(db: Session, user_id: int):
    cart = get_cart_by_user_id(db, user_id)

    if cart is None:
        cart = create_cart(db, user_id)

    return cart


def get_cart_item(
    db: Session,
    cart_id: int,
    product_id: int,
):
    return (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id,
        )
        .first()
    )


def add_cart_item(
    db: Session,
    cart_id: int,
    product_id: int,
    quantity: int,
):
    item = get_cart_item(
        db,
        cart_id,
        product_id,
    )

    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
        )
        db.add(item)

    db.commit()
    db.refresh(item)

    return item


def update_cart_item(
    db: Session,
    item: CartItem,
    quantity: int,
):
    item.quantity = quantity

    db.commit()
    db.refresh(item)

    return item


def delete_cart_item(
    db: Session,
    item: CartItem,
):
    db.delete(item)
    db.commit()