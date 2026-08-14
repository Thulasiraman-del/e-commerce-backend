from sqlalchemy.orm import Session

from app.models.payment import Payment


def create_payment(
    db: Session,
    order_id: int,
    amount,
    payment_method: str,
):
    payment = Payment(
        order_id=order_id,
        amount=amount,
        status="pending",
        payment_method=payment_method,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


def get_payment_by_order_id(
    db: Session,
    order_id: int,
):
    return (
        db.query(Payment)
        .filter(Payment.order_id == order_id)
        .first()
    )


def update_payment_status(
    db: Session,
    payment: Payment,
    status: str,
    transaction_id: str | None = None,
):
    payment.status = status

    if transaction_id is not None:
        payment.transaction_id = transaction_id

    db.commit()
    db.refresh(payment)

    return payment