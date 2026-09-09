from fastapi import FastAPI, HTTPException
from typing import List, Optional
from models import Event
from datetime import date

proj = FastAPI(title="AI Event Assistant")

events_db: List[Event] = [
    Event(
        id=1,
        title="AI Bootcamp",
        event_date="2025-10-24",
        organizer="Tech Club",
        city="Bangalore",
        email="host@techclub.com"
    ),
    Event(
        id=2,
        title="AI Webinar 2025",
        event_date="2025-11-30",
        organizer="XYZ Tech",
        city="Chennai",
        email="support@xyztech.com"
    )
]

@proj.get("/events", response_model=List[Event])
def get_all_events():
    return events_db

@proj.get("/events/search", response_model=List[Event])
def search_events(title: str, city: str = "Bangalore"):
    result = [
        event for event in events_db
        if title.lower() in event.title.lower() and event.city.lower() == city.lower()
    ]
    if result:
        return result
    raise HTTPException(
        status_code=404,
        detail=f"No events found with title containing '{title}' and city as {city}"
    )

@proj.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int):
    for event in events_db:
        if event.id == event_id:
            return event
    raise HTTPException(status_code=404, detail=f"Event with id {event_id} is not available.")

@proj.post("/events/add", response_model=Event)
def create_event(
    event_id: int,
    title: str,
    event_date: date = date.today(),
    organizer: Optional[str] = None,
    email: Optional[str] = None,
    city: str = "Bangalore"
):
    for event in events_db:
        if event.id == event_id:
            raise HTTPException(status_code=400, detail=f"Event ID {event_id} already exists!!!")
    event = Event(
        id=event_id,
        title=title,
        event_date=event_date,
        organizer=organizer,
        city=city,
        email=email
    )
    events_db.append(event)
    return event

@proj.put("/events/replace/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    title: str,
    event_date: date = date.today(),
    organizer: Optional[str] = None,
    email: Optional[str] = None,
    city: str = "Bangalore"
):
    for i, event in enumerate(events_db):
        if event.id == event_id:
            updated_event = Event(
                id=event_id,
                title=title,
                event_date=event_date,
                organizer=organizer,
                city=city,
                email=email
            )
            events_db[i] = updated_event
            return updated_event
    raise HTTPException(status_code=404, detail="Event not found")

@proj.delete("/events/{event_id}")
def delete_event(event_id: int, user_role: str = "participant"):
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to delete events")
    for event in events_db:
        if event_id == event.id:
            events_db.remove(event)
            return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=404, detail="Event not found")
