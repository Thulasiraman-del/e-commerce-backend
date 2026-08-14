from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.cart_repository import get_cart_by_user_id
from app.repositories.order_repository import (
    create_order,
    create_order_item,
    get_order_by_id,
    get_orders_by_user,
)


def create_order_from_cart(
    db: Session,
    user_id: int,
):
    cart = get_cart_by_user_id(
        db,
        user_id,
    )

    if cart is None or not cart.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty",
        )

    total_amount = Decimal("0.00")

    # Validate stock and calculate total
    for cart_item in cart.items:
        product = (
            db.query(Product)
            .filter(Product.id == cart_item.product_id)
            .first()
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product {cart_item.product_id} not found",
            )

        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}",
            )

        unit_price = Decimal(str(product.price))

        total_amount += unit_price * cart_item.quantity

    # Create order
    order = create_order(
        db=db,
        user_id=user_id,
        total_amount=total_amount,
    )

    # Create order items and reduce stock
    for cart_item in list(cart.items):
        product = (
            db.query(Product)
            .filter(Product.id == cart_item.product_id)
            .first()
        )

        unit_price = Decimal(str(product.price))

        subtotal = unit_price * cart_item.quantity

        create_order_item(
            db=db,
            order_id=order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )

        product.stock -= cart_item.quantity

        # Remove purchased item from cart
        db.delete(cart_item)

    db.commit()
    db.refresh(order)

    return get_order_by_id(
        db,
        order.id,
    )


def get_user_orders(
    db: Session,
    user_id: int,
):
    return get_orders_by_user(
        db,
        user_id,
    )


def get_user_order(
    db: Session,
    user_id: int,
    order_id: int,
):
    order = get_order_by_id(
        db,
        order_id,
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if order.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this order",
        )

    return order


def update_user_order_status(
    db: Session,
    user_id: int,
    order_id: int,
    new_status: str,
):
    allowed_statuses = {
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled",
    }

    new_status = new_status.lower().strip()

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid order status. Allowed statuses: "
                "pending, confirmed, shipped, delivered, cancelled"
            ),
        )

    order = get_order_by_id(
        db,
        order_id,
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if order.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this order",
        )

    if order.status == "delivered":
        raise HTTPException(
            status_code=400,
            detail="Delivered orders cannot be updated",
        )

    if order.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Cancelled orders cannot be updated",
        )

    order.status = new_status

    db.commit()
    db.refresh(order)

    return order