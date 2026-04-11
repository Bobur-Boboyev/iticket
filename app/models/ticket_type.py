import enum
from datetime import datetime

from sqlalchemy import String, ForeignKey, Enum, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class TIcketTypeEnum(str, enum.Enum):
    STANDART = "standard"
    VIP = "vip"
    VVIP = "vvip"


class TicketType(Base, TimestampMixin):
    __tablename__ = "ticket_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[TIcketTypeEnum] = mapped_column(Enum(TIcketTypeEnum), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))

    event: Mapped["Event"] = relationship(back_populates="ticket_types")
