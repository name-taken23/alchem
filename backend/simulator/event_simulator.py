import random
import time
from datetime import datetime
import requests

DATABASE_SERVICE_URL = "http://localhost:8001/database"

SAMPLE_EVENTS = [
    "User Login",
    "File Upload",
    "System Error",
    "Data Export",
    "User Logout",
    "Backup Complete"
]

def create_event(event_name, status):
    event_data = {
        "event_name": event_name,
        "status": status,
        "last_updated": datetime.now().isoformat()
    }
    response = requests.post(f"{DATABASE_SERVICE_URL}/events", json=event_data)
    if response.status_code == 201:
        print(f"Added event: {event_name}, Status: {status}, Last Updated: {event_data['last_updated']}")
    else:
        print(f"Failed to add event: {response.json()}")

def update_event(event_id, new_status):
    event_update = {"status": new_status}
    response = requests.put(f"{DATABASE_SERVICE_URL}/events/{event_id}", json=event_update)
    if response.status_code == 200:
        print(f"Updated event ID {event_id}, New Status: {new_status}")
    else:
        print(f"Failed to update event ID {event_id}: {response.json()}")

def simulate_event():
    if random.choice([True, False]):
        event_name = random.choice(SAMPLE_EVENTS)
        status = random.choice(["Pending", "In Progress", "Completed"])
        create_event(event_name, status)
    else:
        response = requests.get(f"{DATABASE_SERVICE_URL}/events")
        if response.status_code == 200 and response.json().get("events"):
            events = response.json()["events"]
            random_event = random.choice(events)
            event_id = random_event["id"]
            new_status = random.choice(["Pending", "In Progress", "Completed"])
            update_event(event_id, new_status)
        else:
            print("No events found to update or failed to fetch events.")

def run_simulator():
    while True:
        simulate_event()
        time.sleep(5)

if __name__ == "__main__":
    run_simulator()
