import enum
from pydantic import BaseModel, Field

from app.models.order import PaymentMethod


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class CreateOrder(BaseModel):
    ticket_type_id: int = Field(gt=0)


class OrderItemResponse(BaseModel):
    id: int
    ticket_id: int
    ticket_type_id: int

    model_config = {
        "from_attributes": True
    }

class OrderResponse(BaseModel):
    id: int
    payment_method: str | None
    user_id: int
    status: OrderStatus
    order_items: list[OrderItemResponse]

    model_config = {
        "from_attributes": True
    }

class UserOrdersResponse(BaseModel):
    user_id: int
    orders: list[OrderResponse]


class PaymentData(BaseModel):
    payment_method: PaymentMethod
    payment_reference: str = Field(max_length=100)