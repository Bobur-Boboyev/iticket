import enum
from datetime import datetime

from sqlalchemy import String, ForeignKey, Enum, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="SET NULL"), nullable=False
    )
    ticket_type_id: Mapped[int] = mapped_column(
        ForeignKey("ticket_types.id"), nullable=False
    )

    order: Mapped["Order"] = relationship(back_populates="items")
    ticket_type: Mapped["TicketType"] = relationship()
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="order_item")
