from pydantic import UUID4, BaseModel

class TicketResponse(BaseModel):
    id: int
    event_id: int
    ticket_type_id: int
    user_id: int
    status: str
    code: UUID4