from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Define the Event model
class Event(BaseModel):
    id: int
    event_name: str
    status: str
    last_updated: datetime

# Model for creating a new event
class EventCreate(BaseModel):
    event_name: str
    status: str
    last_updated: datetime

# Model for updating an event's status
class EventUpdate(BaseModel):
    status: str

# Model for paginated response
class PaginatedEvents(BaseModel):
    events: list[Event]
    total_count: int

# Base URL for the database service
DATABASE_SERVICE_URL = "http://localhost:8001"

# Fetch all events asynchronously with pagination
@app.get("/api/events", response_model=PaginatedEvents)
async def get_events(page: int = 1, page_size: int = 10):
    params = {"page": page, "page_size": page_size}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATABASE_SERVICE_URL}/database/events", params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching events")
    return response.json()

# Create a new event asynchronously
@app.post("/api/events", status_code=201)
async def create_event(event: EventCreate):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DATABASE_SERVICE_URL}/database/events", json=event.dict())
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Error creating event")
    return response.json()

# Update an event's status asynchronously
@app.put("/api/events/{event_id}")
async def update_event_status(event_id: int, event_update: EventUpdate):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{DATABASE_SERVICE_URL}/database/events/{event_id}", json=event_update.dict()
        )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Event not found")
    elif response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error updating event")
    return response.json()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Adjust to match frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
