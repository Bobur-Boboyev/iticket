from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id", ondelete="SET NULL"), nullable=True)

    category: Mapped["Category"] = relationship(back_populates="events")
    venue: Mapped["Venue"] = relationship(back_populates="events")
    ticket_types: Mapped[list["TicketType"]] = relationship(back_populates="event")
