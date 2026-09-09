from datetime import date
from typing import Optional
from pydantic import BaseModel

class Event(BaseModel):
    id: int
    title: str
    event_date: date
    organizer: Optional[str] = None
    city: str
    email: Optional[str] = None

    def __init__(self, id: int, title: str, event_date: date,
                 organizer: Optional[str] = None, city: str = "Bangalore",
                 email: Optional[str] = None):
        super().__init__(
            id=id,
            title=title,
            event_date=event_date,
            organizer=organizer,
            city=city,
            email=email
        )