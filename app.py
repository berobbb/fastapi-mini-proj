from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from models import Event
proj = FastAPI()


@proj.post("/event/add")
def create_event(event:Event):
    return {"message": "Event created", "event": event}