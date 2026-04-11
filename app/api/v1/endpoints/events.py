from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body, Query
from sqlalchemy.orm import Session

from app.services.event_service import EventService
from app.schemas.event import CreateEvent, EVentFilter, EventResponse, UpdateEvent
from app.core.security import get_admin
from app.db.session import get_db
from app.models.user import User


router = APIRouter(
    prefix="/events",
    tags=["events"],
)


@router.get("/", response_model=list[EventResponse])
async def events_view(
    filter_params: Annotated[EVentFilter, Query()],
    db: Annotated[Session, Depends(get_db)],
):
    event_service = EventService(db)
    events = event_service.get_events(filter_params)

    return events


@router.get("/{id}", response_model=EventResponse)
async def get_event_view(
    id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
):
    event_service = EventService(db)
    event = event_service.get_event_by_id(id)

    return event


@router.post("/", response_model=EventResponse)
async def create_event_view(
    data: Annotated[CreateEvent, Body()],
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    event_service = EventService(db)
    event = event_service.create_event(data)

    return event


@router.patch("/{id}", response_model=EventResponse)
async def update_event_view(
    id: Annotated[int, Path()],
    data: Annotated[UpdateEvent, Body()],
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    event_service = EventService(db)
    event = event_service.update_event(id, data)

    return event


@router.delete("/{id}", status_code=204)
async def delete_event_view(
    id: Annotated[int, Path()],
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    event_service = EventService(db)
    event_service.delete_event(id)
