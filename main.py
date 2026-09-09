from fastapi import FastAPI
import uvicorn

app=FastAPI()
@app.get("/")
def homepage():
    return "hey there"
@app.get("/welcome/{organizer_name}")
def greet(organizer_name:str):
    return f"Welcome {organizer_name} to Event Organizer Portal"

@app.get("/event-count")
def event_count(year:int):
    return f"Number of events planned in {year} : 5"
if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)

