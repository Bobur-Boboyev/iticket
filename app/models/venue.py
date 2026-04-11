from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Venue(Base, TimestampMixin):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    location: Mapped[str] = mapped_column(String(255))

    events: Mapped[list["Event"]] = relationship(back_populates="venue")
