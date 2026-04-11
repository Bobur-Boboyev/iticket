from pydantic import BaseModel


class VenueResponse(BaseModel):
    id: int
    name: str
    location: str

class CreateVenue(BaseModel):
    name: str
    location: str

class UpdateVenue(BaseModel):
    name: str | None = None
    location: str | None = None