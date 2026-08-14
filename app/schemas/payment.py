from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    payment_method: str


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: Decimal
    status: str
    payment_method: str
    transaction_id: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)