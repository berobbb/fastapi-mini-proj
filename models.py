from datetime import date
from typing import Optional
from pydantic import BaseModel,EmailStr,Field,field_validator

class Event(BaseModel):
    id: int
    title: str=Field(min_length=2,max_length=50)
    event_date: date
    organizer: Optional[str] = None
    city: str
    email: EmailStr
    @field_validator("event_date")      # field validator for event date
    @classmethod
    def check_future_date(cls, value):
        if value < date.today():
            raise ValueError("Event date cannot be in the past")
        return value