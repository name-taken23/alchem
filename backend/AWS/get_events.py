import json
import boto3
import os
from boto3.dynamodb.conditions import Key

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE', 'events')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):

    page_size = int(event.get("queryStringParameters", {}).get("page_size", 10))
    last_evaluated_key = event.get("queryStringParameters", {}).get("last_evaluated_key", None)
    
    scan_kwargs = {
        'Limit': page_size,
    }
    
    if last_evaluated_key:
        scan_kwargs['ExclusiveStartKey'] = json.loads(last_evaluated_key)
    
    try:
        response = table.scan(**scan_kwargs)
        events = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey', None)

        body = {
            'events': events,
            'last_evaluated_key': json.dumps(last_evaluated_key) if last_evaluated_key else None
        }

        return {
            'statusCode': 200,
            'body': json.dumps(body)
        }

    except Exception as e:
        print(f"Error fetching events: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Error fetching events"})
        }
