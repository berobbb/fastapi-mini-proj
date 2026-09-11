# AI Event Assistant — FastAPI CRUD API

A simple REST API built using **FastAPI** and **SQLAlchemy** for managing events.

The project demonstrates the complete **CRUD (Create, Read, Update, Delete)** workflow along with database connectivity, Pydantic schemas, SQLAlchemy ORM models, and FastAPI dependency injection.

---

## 🛠️ Technologies Used

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* Uvicorn

---

## 📁 Project Structure

```text
project/
│
├── main.py
├── models.py
├── schema.py
├── config.py
├── database.db
└── README.md
```

### `main.py`

Contains the FastAPI application and CRUD API endpoints.

### `models.py`

Contains SQLAlchemy ORM models representing database tables.

### `schema.py`

Contains Pydantic schemas used for request validation.

### `config.py`

Contains database configuration, SQLAlchemy engine, session factory, and database dependency.

---

# 🔌 Database Configuration

The project uses SQLite.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///company.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
```

---

# 🔄 Database Dependency

A database session is created for each request and closed after the request finishes.

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

### Why `yield`?

`yield` provides the database session to the API endpoint.

After the request is completed, the `finally` block closes the session.

---

# 🗃️ SQLAlchemy Model

Example `Event` model:

```python
from sqlalchemy import Column, Integer, String, Date
from database import Base

class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    organizer = Column(String)
    city = Column(String)
    email = Column(String)
```

The SQLAlchemy model represents the database table.

```text
Python Class  → Database Table
Object        → Database Row
Attribute     → Database Column
```

---

# 📝 Pydantic Schema

The Pydantic schema validates incoming API data.

```python
from pydantic import BaseModel
from datetime import date

class EventSchema(BaseModel):

    id: int | None = None
    title: str
    date: date
    organizer: str
    city: str
    email: str
```

---

# 🚀 FastAPI Application

```python
from fastapi import FastAPI, HTTPException, Depends
from schema import EventSchema
from models import Event
from config import SessionLocal, get_db
from datetime import date

app = FastAPI(title="AI Event Assistant")
```

---

# ➕ CREATE — Add Event

### Endpoint

```text
POST /events/add
```

### Code

```python
@app.post("/events/add")
def create_event(
    event: EventSchema,
    db = Depends(get_db)
):

    new_event = Event(**event.__dict__)

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "message": "Event created successfully",
        "event": new_event
    }
```

### Flow

```text
Request
   ↓
Pydantic validation
   ↓
Create SQLAlchemy object
   ↓
db.add()
   ↓
db.commit()
   ↓
db.refresh()
   ↓
Response
```

---

# 📖 READ — Get All Events

### Endpoint

```text
GET /events
```

### Code

```python
@app.get("/events")
def get_all_events(db = Depends(get_db)):

    return db.query(Event).all()
```

`all()` returns all matching records as a list.

---

# 🔎 READ — Get Event by ID

### Endpoint

```text
GET /events/{event_id}
```

### Code

```python
@app.get("/events/{event_id}")
def get_event(
    event_id: int,
    db = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return {
        "event details": event
    }
```

### Important SQLAlchemy methods

```text
query()   → choose model/table
filter()  → apply condition
first()   → get first matching record
```

---

# 📅 READ — Upcoming Events

### Endpoint

```text
GET /events/upcoming
```

### Code

```python
@app.get("/events/upcoming")
def upcoming_events(db = Depends(get_db)):

    today = date.today()

    upcoming = (
        db.query(Event)
        .filter(Event.date >= today)
        .order_by(Event.date)
        .all()
    )

    return {
        "upcoming_events": upcoming
    }
```

This retrieves events whose date is today or later and sorts them by date.

---

# ✏️ UPDATE — Update Event

### Endpoint

```text
PUT /events/change/{event_id}
```

### Code

```python
@app.put("/events/change/{event_id}")
def update_event(
    event_id: int,
    event: EventSchema,
    db = Depends(get_db)
):

    upd_event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not upd_event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    upd_event.title = event.title
    upd_event.date = event.date
    upd_event.organizer = event.organizer
    upd_event.city = event.city
    upd_event.email = event.email

    db.commit()
    db.refresh(upd_event)

    return {
        "message": "Event updated",
        "event": upd_event
    }
```

### Update flow

```text
Find existing object
        ↓
Modify attributes
        ↓
db.commit()
        ↓
db.refresh()
```

---

# 🗑️ DELETE — Cancel Event

### Endpoint

```text
DELETE /events/cancel/{event_id}
```

### Code

```python
@app.delete("/events/cancel/{event_id}")
def cancel_event(
    event_id: int,
    db = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    db.delete(event)
    db.commit()

    return {
        "message": f"Event with ID {event_id} cancelled"
    }
```

---

# 🔄 CRUD Summary

| Operation | HTTP Method | Endpoint              | SQLAlchemy              |
| --------- | ----------- | --------------------- | ----------------------- |
| Create    | POST        | `/events/add`         | `add()` + `commit()`    |
| Read All  | GET         | `/events`             | `query().all()`         |
| Read One  | GET         | `/events/{id}`        | `filter().first()`      |
| Update    | PUT         | `/events/change/{id}` | Modify + `commit()`     |
| Delete    | DELETE      | `/events/cancel/{id}` | `delete()` + `commit()` |

---

# 🧠 Important SQLAlchemy Concepts

### `db.add()`

Adds an object to the current session.

```python
db.add(new_event)
```

### `db.commit()`

Saves the transaction to the database.

```python
db.commit()
```

### `db.refresh()`

Reloads the object from the database.

```python
db.refresh(new_event)
```

Useful when the database generates values such as an ID.

### `db.delete()`

Marks an object for deletion.

```python
db.delete(event)
```

### `db.rollback()`

Cancels uncommitted changes when an error occurs.

```python
try:
    db.add(event)
    db.commit()
except:
    db.rollback()
```

### `db.close()`

Closes the database session.

```python
db.close()
```

---

# 🔍 Query Examples

### Get everything

```python
db.query(Event).all()
```

### Get one

```python
db.query(Event).filter(Event.id == 1).first()
```

### Filter

```python
db.query(Event).filter(
    Event.city == "Delhi"
).all()
```

### Multiple conditions

```python
db.query(Event).filter(
    Event.city == "Delhi",
    Event.organizer == "ABC"
).all()
```

### Sort ascending

```python
db.query(Event).order_by(Event.date).all()
```

### Sort descending

```python
db.query(Event).order_by(
    Event.date.desc()
).all()
```

### Count records

```python
db.query(Event).count()
```

---

# 🔗 SQLAlchemy Relationships

Relationships allow different database tables to be connected.

### One-to-Many

Example:

```text
User
 ↓
Many Events
```

```python
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    events = relationship(
        "Event",
        back_populates="user"
    )


class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="events"
    )
```

Important:

```text
ForeignKey()
    → database-level relationship

relationship()
    → Python/ORM-level relationship
```

---

# 🧩 FastAPI + SQLAlchemy Architecture

```text
              Client
                │
                ▼
             FastAPI
                │
                ▼
        Pydantic Schema
        (Validation)
                │
                ▼
       SQLAlchemy ORM Model
                │
                ▼
             Session
                │
                ▼
             SQLite
             Database
```

---

# 🆚 Pydantic vs SQLAlchemy

| Pydantic              | SQLAlchemy           |
| --------------------- | -------------------- |
| API validation        | Database interaction |
| Request/response data | Database models      |
| Validates input       | Queries database     |
| `BaseModel`           | `DeclarativeBase`    |
| API layer             | Database layer       |

---

# ▶️ Running the Project

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy
```

Start the application:

```bash
uvicorn main:app --reload
```

The API will run on:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🎯 Interview Questions

### 1. What is SQLAlchemy?

SQLAlchemy is a Python SQL toolkit and ORM that allows Python applications to interact with relational databases.

### 2. What is a Session?

A Session manages database interactions and transactions for ORM objects.

### 3. What does `db.commit()` do?

It commits the current transaction and persists changes to the database.

### 4. Why use `db.refresh()`?

To reload the object with the latest database state, including generated values such as IDs.

### 5. Why use `Depends(get_db)`?

It provides a database session to the FastAPI endpoint and ensures the session is properly closed.

### 6. Difference between `filter()` and `filter_by()`?

```python
filter(Event.id == 1)
```

uses SQLAlchemy expressions, while:

```python
filter_by(id=1)
```

uses keyword-based filtering.

### 7. Difference between `all()` and `first()`?

```text
all()   → list of results
first() → first result or None
```

### 8. Why should we not use one global database Session?

Because sessions are meant to be managed per unit of work/request. A global session can cause stale state, transaction conflicts, and concurrency problems.

---

# 📌 Complete CRUD Flow

```text
                FASTAPI
                   │
        ┌──────────┼──────────┐
        │          │          │
       POST       GET        PUT/DELETE
        │          │          │
        ▼          ▼          ▼
     CREATE      READ      UPDATE/DELETE
        │          │          │
        └──────────┼──────────┘
                   ▼
              SQLAlchemy
                   │
                 Session
                   │
                   ▼
                SQLite
```

## Key Things to Remember

```text
FastAPI
   → API framework

Pydantic
   → Validation

SQLAlchemy
   → Database / ORM

Session
   → Database interaction + transactions

Engine
   → Database connectivity

Model
   → Database table representation

CRUD
   → Create, Read, Update, Delete
```
