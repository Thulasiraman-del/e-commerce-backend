from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.order import (
    OrderResponse,
    OrderStatusUpdate,
)
from app.services.order_service import (
    create_order_from_cart,
    get_user_order,
    get_user_orders,
    update_user_order_status,
)


router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"],
)


@router.post(
    "/",
    response_model=OrderResponse,
)
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_order_from_cart(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[OrderResponse],
)
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_orders(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_order(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
    )


@router.put(
    "/{order_id}/status",
    response_model=OrderResponse,
)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_user_order_status(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
        new_status=status_data.status,
    )