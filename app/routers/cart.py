from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.cart import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
)
from app.services.cart_service import (
    add_product_to_cart,
    get_user_cart,
    remove_product_from_cart,
    update_product_quantity,
)

router = APIRouter(
    prefix="/api/cart",
    tags=["Cart"],
)


@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_cart(
        db=db,
        user_id=current_user.id,
    )


@router.post(
    "/items",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_item(
    data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_product_to_cart(
        db=db,
        user_id=current_user.id,
        product_id=data.product_id,
        quantity=data.quantity,
    )


@router.put(
    "/items/{product_id}",
    response_model=CartItemResponse,
)
def update_item(
    product_id: int,
    data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_product_quantity(
        db=db,
        user_id=current_user.id,
        product_id=product_id,
        quantity=data.quantity,
    )


@router.delete(
    "/items/{product_id}",
)
def remove_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    remove_product_from_cart(
        db=db,
        user_id=current_user.id,
        product_id=product_id,
    )

    return {
        "message": "Product removed from cart"
    }