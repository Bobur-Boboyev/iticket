from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Event, TicketType, Venue

from app.schemas.event import CreateEvent, UpdateEvent, EVentFilter


class EventService:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, data: CreateEvent) -> Event:
        existing = self.get_event_by_title(data.title)
        if existing:
            raise HTTPException(
                status_code=400, detail="Event with this title already exists"
            )

        event = Event(
            title=data.title,
            date=data.date,
            category_id=data.category_id,
            venue_id=data.venue_id,
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        if data.ticket_types:
            ticket_types = []
            for tt in data.ticket_types:
                ticket_type = TicketType(
                    name=tt.name,
                    price=tt.price,
                    quantity=tt.quantity,
                    event_id=event.id,
                )
                ticket_types.append(ticket_type)
            self.db.add_all(ticket_types)
            self.db.commit()

        return event

    def update_event(self, id: int, data: UpdateEvent):
        event = self.get_event_by_id(id)

        if data.title and data.title != event.title:
            existing = self.get_event_by_title(data.title)
            if existing and existing.id != id:
                raise HTTPException(
                    status_code=400, detail="Event with this title already exists"
                )
            event.title = data.title
        if data.date is not None:
            event.date = data.date
        if data.category_id is not None:
            event.category_id = data.category_id
        if data.venue_id is not None:
            event.venue_id = data.venue_id

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        if data.ticket_types is not None:
            self.db.query(TicketType).filter(TicketType.event_id == id).delete()
            self.db.commit()

            ticket_types = []
            for tt in data.ticket_types:
                ticket_type = TicketType(
                    name=tt.name,
                    price=tt.price,
                    quantity=tt.quantity,
                    event_id=event.id,
                )
                ticket_types.append(ticket_type)
            self.db.add_all(ticket_types)
            self.db.commit()

        return event

    def get_events(self, filter_params: EVentFilter):
        query = self.db.query(Event)

        if filter_params.category_id:
            query = query.filter(Event.category_id == filter_params.category_id)
        if filter_params.active_only:
            query = query.filter(Event.date >= datetime.now())
        if filter_params.city:
            query = query.join(Event.venue).filter(
                Venue.location.ilike(f"%{filter_params.city}%")
            )
        if filter_params.page and filter_params.page_size:
            offset = (filter_params.page - 1) * filter_params.page_size
            query = query.offset(offset).limit(filter_params.page_size)

        return query.all()

    def delete_event(self, id):
        event = self.get_event_by_id(id)
        self.db.query(TicketType).filter(TicketType.event_id == id).delete()
        self.db.commit()

        event = self.get_event_by_id(id)
        self.db.delete(event)
        self.db.commit()

    def get_event_by_id(self, id):
        event = self.db.query(Event).filter(Event.id == id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    def get_event_by_title(self, title):
        return self.db.query(Event).filter(Event.title == title).first()

    def get_all_events(self):
        return self.db.query(Event).all()
