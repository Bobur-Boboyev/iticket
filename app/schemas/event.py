import enum
from datetime import datetime

from pydantic import BaseModel, Field, model_validator, field_validator, EmailStr


class TicetTypeEnum(str, enum.Enum):
    STANDART = "standard"
    VIP = "vip"
    VVIP = "vvip"


class TicketQuantity(BaseModel):
    name: TicetTypeEnum
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


class CreateEvent(BaseModel):
    title: str = Field(max_length=150)
    date: datetime
    category_id: int = Field(gt=0)
    venue_id: int = Field(gt=0)

    ticket_types: list[TicketQuantity]

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class UpdateEvent(BaseModel):
    title: str | None = Field(default=None, max_length=150)
    date: datetime | None = None
    category_id: int | None = Field(default=None, gt=0)
    venue_id: int | None = Field(default=None, gt=0)

    ticket_types: list[TicketQuantity] | None = None


class EventResponse(BaseModel):
    id: int
    title: str
    date: datetime
    category_id: int
    venue_id: int

    ticket_types: list[TicketQuantity]
