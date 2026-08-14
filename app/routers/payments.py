from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import (
    create_order_payment,
    get_order_payment,
    complete_order_payment,
)


router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"],
)


@router.post(
    "/{order_id}",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    order_id: int,
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_order_payment(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
        payment_data=payment_data,
    )


@router.get(
    "/{order_id}",
    response_model=PaymentResponse,
)
def get_payment(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_order_payment(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
    )


@router.put(
    "/{payment_id}/complete",
    response_model=PaymentResponse,
)
def complete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return complete_order_payment(
        db=db,
        user_id=current_user.id,
        payment_id=payment_id,
    )