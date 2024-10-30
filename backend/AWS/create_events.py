import json
import boto3
import os
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE', 'events')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:

        body = json.loads(event["body"])
        event_name = body["event_name"]
        status = body["status"]
        last_updated = datetime.now().isoformat()


        event_id = str(uuid.uuid4())


        table.put_item(
            Item={
                "id": event_id,
                "event_name": event_name,
                "status": status,
                "last_updated": last_updated
            }
        )

        return {
            'statusCode': 201,
            'body': json.dumps({"id": event_id, "message": "Event created successfully"})
        }

    except Exception as e:
        print(f"Error creating event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Error creating event"})
        }
