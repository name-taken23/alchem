import random
import time
import json
from datetime import datetime
import boto3

# Initialize the Lambda client
lambda_client = boto3.client("lambda")

# Lambda function names
CREATE_EVENT_FUNCTION = "create_event_lambda"
UPDATE_EVENT_FUNCTION = "update_event_lambda"
FETCH_EVENTS_FUNCTION = "fetch_events_lambda"

# Event data for simulation
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
    response = lambda_client.invoke(
        FunctionName=CREATE_EVENT_FUNCTION,
        InvocationType="RequestResponse",
        Payload=json.dumps({"body": json.dumps(event_data)})
    )
    result = json.loads(response["Payload"].read())
    if response["StatusCode"] == 200:
        print(f"Added event: {event_name}, Status: {status}, Last Updated: {event_data['last_updated']}")
    else:
        print(f"Failed to add event: {result}")

def update_event(event_id, new_status):
    event_update = {"status": new_status}
    response = lambda_client.invoke(
        FunctionName=UPDATE_EVENT_FUNCTION,
        InvocationType="RequestResponse",
        Payload=json.dumps({
            "pathParameters": {"event_id": event_id},
            "body": json.dumps(event_update)
        })
    )
    result = json.loads(response["Payload"].read())
    if response["StatusCode"] == 200:
        print(f"Updated event ID {event_id}, New Status: {new_status}")
    else:
        print(f"Failed to update event ID {event_id}: {result}")

def fetch_events():
    response = lambda_client.invoke(
        FunctionName=FETCH_EVENTS_FUNCTION,
        InvocationType="RequestResponse",
        Payload=json.dumps({
            "queryStringParameters": {"page": "1", "page_size": "10"}
        })
    )
    result = json.loads(response["Payload"].read())
    if response["StatusCode"] == 200 and result.get("events"):
        return result["events"]
    else:
        print("No events found to update or failed to fetch events.")
        return []

def simulate_event():
    if random.choice([True, False]):
        event_name = random.choice(SAMPLE_EVENTS)
        status = random.choice(["Pending", "In Progress", "Completed"])
        create_event(event_name, status)
    else:
        events = fetch_events()
        if events:
            random_event = random.choice(events)
            event_id = random_event["id"]
            new_status = random.choice(["Pending", "In Progress", "Completed"])
            update_event(event_id, new_status)

def run_simulator():
    while True:
        simulate_event()
        time.sleep(5) 

if __name__ == "__main__":
    run_simulator()
