import enum
from datetime import datetime

from sqlalchemy import String, ForeignKey, Enum, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentMethod(str, enum.Enum):
    CREDIT_CARD = "credit_card"
    CASH = "cash"

class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.PENDING
    )
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
