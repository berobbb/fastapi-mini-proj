from fastapi import FastAPI, HTTPException
from typing import List
from models import Event
from datetime import date

proj = FastAPI(title="AI Event Assistant")
events_db: List[Event] = [
    Event(
        id=1,
        title="AI Bootcamp",
        date="2025-10-24",
        organizer="Tech Club",
        city="Bangalore",
        email="host@techclub.com"
    ),
    Event(
        id=2,
        title="AI Webinar 2025",
        date="2025-11-30",
        organizer="XYZ Tech",
        city="Chennai",
        email="support@xyztech.com"
    )
]
@proj.get("/events")
def get_all_events():           						# Fetch all events
    return events_db
@proj.get("/events/search")
def search_events(title: str, city: str="Bangalore"):   # Fetch event by title and city
    result = []
    for event in events_db:
        if event.title.lower().count(title.lower())>0 and event.city.lower() == city.lower():
            result.append(event)
    if len(result)>0:
        return result
    return {"message": "No events found with title containing '"+title+"' and city as "+city}
@proj.get("/events/{event_id}")
def get_event(event_id: int):       					# Fetch event by ID
    for event in events_db:
        if event.id == event_id:
            return {"event details": event}
    return {"message": "Event with id "+str(event_id)+" is not available."}

@proj.post("/events/add")
def create_event(event_id:int, title:str, date:date=date.today(), organizer:str=None, email:str=None, city:str="Bangalore"):
    for event in events_db:
        if event.id == event_id:
            return {"ERROR!!!":"Event ID "+str(event_id)+" already exists!!!"}
    event = Event(event_id,title,date,organizer,city,email)
    events_db.append(event)
    return {"message": "Event created successfully", "event": event}
@proj.put("/events/replace/{event_id}")
def update_event(event_id: int, title:str, date:date=date.today(), organizer:str=None, email:str=None, city:str="Bangalore"):
    for i, event in enumerate(events_db):
        if event.id == event_id:
            updated_event = Event(event_id,title,date,organizer,city,email)
            events_db[i] = updated_event
            return {"message": "Event updated", "event": updated_event}
    return {"error": "Event not found"}
@proj.patch("/events/edit/{event_id}")
def change_event(event_id: int,title:str=None, date:date=None, organizer:str=None, city:str=None, email:str=None):
    for i, event in enumerate(events_db):
        if event.id == event_id:
            if title!=None:
                event.title = title
            if date!=None:
                event.date = date
            if organizer!=None:
                event.organizer = organizer
            if city!=None:
                event.city = city
            if email!=None:
                event.email = email
            return {"message": "Event updated", "event": event}
    return {"error": "Event not found"}
@proj.delete("/events/cancel/{event_id}")
def delete_event(event_id: int):
    for event in events_db:
        if event.id == event_id:
            events_db.remove(event)
            return {"message": f"Event with id {event_id} deleted"}
    return {"error": "Event not found"}

