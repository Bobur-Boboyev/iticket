from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Ticket, User
from app.models.ticket import TicketStatus
from app.schemas.ticket import TicketResponse


class TicketService:
    def __init__(self, db: Session):
        self.db = db

    def get_tickets_by_user(self, user: User) -> list[TicketResponse]:
        orders = user.orders
        tickets = []
        for order in orders:
            if order.status == "paid":
                for item in order.items:
                    ticket = self.db.query(Ticket).filter(Ticket.id == item.ticket_id).first()
                    if ticket:
                        tickets.append(
                            TicketResponse(
                                id=ticket.id,
                                event_id=item.ticket_type.event_id,
                                ticket_type_id=item.ticket_type_id,
                                user_id=order.user_id,
                                status=TicketStatus(ticket.status).name,
                                code=ticket.code
                            )
                        )
        return tickets
    
    def verify_ticket(self, code: str) -> TicketResponse:
        ticket = self.db.query(Ticket).filter(Ticket.code == code).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        if ticket.status != TicketStatus.SOLD.value:
            raise HTTPException(status_code=400, detail="Ticket is not paid")
        if ticket.status == TicketStatus.USED.value:
            raise HTTPException(status_code=400, detail="Ticket has already been used")
        
        ticket.status = TicketStatus.USED.value
        
        self.db.commit()
        self.db.refresh(ticket)
        
        return TicketResponse(
            id=ticket.id,
            event_id=ticket.order_item.ticket_type.event_id,
            ticket_type_id=ticket.order_item.ticket_type_id,
            user_id=ticket.order_item.order.user_id,
            status=TicketStatus(ticket.status).name,
        )
    
    def create_tickets(self, count: int) -> list[Ticket]:
        tickets = []
        for i in count:
            t = Ticket()
            tickets.append(t)

        return tickets