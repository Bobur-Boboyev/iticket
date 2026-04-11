from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Venue
from app.schemas.venue import VenueResponse


class VenueService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_venues(self) -> list[Venue]:
        return self.db.query(Venue).all()
    
    def get_venue_by_id(self, id: int) -> Venue:
        venue = self.db.query(Venue).filter(Venue.id == id).first()
        if not venue:
            raise HTTPException(status_code=404, detail="Venue not found")
        return venue
    
    def create_venue(self, data: VenueResponse) -> Venue:
        venue = Venue(name=data.name, location=data.location)

        self.db.add(venue)
        self.db.commit()
        self.db.refresh(venue)

        return venue
    
    def update_venue(self, id: int, data: VenueResponse) -> Venue:
        venue = self.get_venue_by_id(id)

        if data.name:
            venue.name = data.name
        if data.location:
            venue.location = data.location

        self.db.commit()
        self.db.refresh(venue)

        return venue
    
    def delete_venue(self, id: int):
        venue = self.get_venue_by_id(id)
        
        self.db.delete(venue)
        self.db.commit()