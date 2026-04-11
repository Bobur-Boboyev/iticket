from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.core.security import get_admin, get_user
from app.db.session import get_db
from app.models import User
from app.services.ticket_service import TicketService
from app.schemas.ticket import TicketResponse



router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

@router.get("/my", response_model=list[TicketResponse])
async def my_tickets_view(
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    ticket_service = TicketService(db)
    tickets = ticket_service.get_tickets_by_user(user)

    return tickets

@router.get("/verify/{code}", response_model=TicketResponse)
async def verify_ticket_view(
    code: Annotated[str, Path()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
):
    ticket_service = TicketService(db)
    ticket = ticket_service.verify_ticket(code)

    return ticket