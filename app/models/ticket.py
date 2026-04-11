import enum
import uuid
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class TicketStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    SOLD = "SOLD"
    CANCELLED = "CANCELLED"
    USED = "USED"


class Ticket(Base, TimestampMixin):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True
    )
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus),
        default=TicketStatus.AVAILABLE
    )

    order_item: Mapped["OrderItem"] = relationship(
        back_populates="tickets"
    )