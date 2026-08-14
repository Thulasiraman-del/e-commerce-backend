from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.payment import Payment
from app.repositories.payment_repository import (
    create_payment,
    get_payment_by_order_id,
    update_payment_status,
)


def create_order_payment(
    db: Session,
    user_id: int,
    order_id: int,
    payment_data,
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == user_id,
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    existing_payment = get_payment_by_order_id(
        db,
        order_id,
    )

    if existing_payment:
        return existing_payment

    return create_payment(
        db=db,
        order_id=order_id,
        amount=order.total_amount,
        payment_method=payment_data.payment_method,
    )


def get_order_payment(
    db: Session,
    user_id: int,
    order_id: int,
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == user_id,
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    payment = get_payment_by_order_id(
        db,
        order_id,
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return payment


def complete_order_payment(
    db: Session,
    user_id: int,
    payment_id: int,
):
    payment = (
        db.query(Payment)
        .join(Order, Payment.order_id == Order.id)
        .filter(
            Payment.id == payment_id,
            Order.user_id == user_id,
        )
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    if payment.status == "completed":
        return payment

    return update_payment_status(
        db,
        payment,
        "completed",
    )