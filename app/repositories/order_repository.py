from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem


def create_order(
    db: Session,
    user_id: int,
    total_amount,
):
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending",
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def get_order_by_id(
    db: Session,
    order_id: int,
):
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )


def get_orders_by_user(
    db: Session,
    user_id: int,
):
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def create_order_item(
    db: Session,
    order_id: int,
    product_id: int,
    quantity: int,
    unit_price,
    subtotal,
):
    item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        subtotal=subtotal,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def update_order_status(
    db: Session,
    order: Order,
    status: str,
):
    order.status = status

    db.commit()
    db.refresh(order)

    return order