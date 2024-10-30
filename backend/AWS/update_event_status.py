import json
import boto3
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE', 'events')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:

        event_id = event["pathParameters"]["event_id"]
        body = json.loads(event["body"])
        new_status = body["status"]
        last_updated = datetime.now().isoformat()
        
        response = table.update_item(
            Key={"id": event_id},
            UpdateExpression="SET #s = :status, last_updated = :last_updated",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":status": new_status,
                ":last_updated": last_updated
            },
            ReturnValues="UPDATED_NEW"
        )
        
        if "Attributes" not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({"error": "Event not found"})
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "Event updated successfully",
                "updated_attributes": response["Attributes"]
            })
        }
        
    except Exception as e:
        print(f"Error updating event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Error updating event"})
        }
