from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from databases import Database
from datetime import datetime
from typing import List
from contextlib import asynccontextmanager

app = FastAPI()

# Initialize the async database connection
DATABASE_URL = "sqlite+aiosqlite:///./database.db"
database = Database(DATABASE_URL)

# Models
class Event(BaseModel):
    id: int
    event_name: str
    status: str
    last_updated: datetime

class EventCreate(BaseModel):
    event_name: str
    status: str
    last_updated: datetime

class EventUpdate(BaseModel):
    status: str

class PaginatedEvents(BaseModel):
    events: List[Event]
    total_count: int

# Lifespan context for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await database.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT,
        status TEXT,
        last_updated TIMESTAMP
    )
    """)
    yield  # Control returns to application
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Fetch paginated events
@app.get("/database/events", response_model=PaginatedEvents)
async def fetch_events(page: int = Query(1, gt=0), page_size: int = Query(10, gt=0)):
    offset = (page - 1) * page_size
    events_query = "SELECT * FROM events LIMIT :limit OFFSET :offset"
    events = await database.fetch_all(query=events_query, values={"limit": page_size, "offset": offset})
    
    count_query = "SELECT COUNT(*) FROM events"
    total_count = await database.fetch_val(query=count_query)

    events_list = [
        Event(
            id=row["id"],
            event_name=row["event_name"],
            status=row["status"],
            last_updated=row["last_updated"]
        ) for row in events
    ]
    
    return PaginatedEvents(events=events_list, total_count=total_count)

@app.post("/database/events", status_code=201)
async def create_event(event: EventCreate):
    query = """
    INSERT INTO events (event_name, status, last_updated)
    VALUES (:event_name, :status, :last_updated)
    """
    event_id = await database.execute(query=query, values=event.dict())
    return {"id": event_id, "message": "Event created successfully"}

@app.put("/database/events/{event_id}")
async def update_event(event_id: int, event_update: EventUpdate):
    query = """
    UPDATE events SET status = :status, last_updated = CURRENT_TIMESTAMP WHERE id = :id
    """
    values = {"status": event_update.status, "id": event_id}
    result = await database.execute(query=query, values=values)
    if result == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event updated successfully"}
