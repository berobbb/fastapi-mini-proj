from pydantic import BaseModel, EmailStr
from datetime import date
class EventSchema(BaseModel):
    id: int
    title: str
    date: date
    organizer: str
    city: str
    email: EmailStr
