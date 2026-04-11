from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_admin
from app.models.user import User
from app.services.venue_service import VenueService
from app.schemas.venue import CreateVenue, VenueResponse, UpdateVenue


router = APIRouter(
    prefix="/venues",
    tags=["venues"],
)

@router.get("/{id}", response_model=VenueResponse)
async def get_venue_view(
    id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
):
    venue_service = VenueService(db)
    venue = venue_service.get_venue_by_id(id)

    return venue

@router.get("/", response_model=list[VenueResponse])
async def venues_view(db: Annotated[Session, Depends(get_db)]):
    venue_service = VenueService(db)
    venues = venue_service.get_all_venues()

    return venues


@router.post("/", response_model=VenueResponse)
async def create_venue_view(
    data: Annotated[CreateVenue, Body()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
):
    venue_service = VenueService(db)
    venue = venue_service.create_venue(data=data)

    return venue

@router.patch("/{id}", response_model=VenueResponse)
async def update_venue_view(
    id: Annotated[int, Path()],
    data: Annotated[UpdateVenue, Body()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
):
    venue_service = VenueService(db)
    venue = venue_service.update_venue(id, data)

    return venue


@router.delete("/{id}", status_code=204)
async def delete_venue_view(
    id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
):
    venue_service = VenueService(db)
    venue_service.delete_venue(id)