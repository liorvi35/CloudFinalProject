import json
import boto3

DYNAMO_DB_SERVICE = "dynamodb"
S3_SERVICE = "s3"
TABLE_NAME = "SN-Users"
BUCKET_NAME = "sn-profile-pictures"  # Replace with your bucket name

def lambda_handler(event, context):
    try:
        # Extract accountID from the event
        account_id = event.get("accountID")
        if not account_id:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "body": "Bad Request"
            }

        # Initialize DynamoDB and S3 clients
        dynamodb = boto3.resource(DYNAMO_DB_SERVICE)
        table = dynamodb.Table(TABLE_NAME)
        s3 = boto3.client(S3_SERVICE)

        # Check if the item exists in DynamoDB
        check_existing = table.get_item(
            Key={"accountID": account_id}
        )
        
        if "Item" not in check_existing:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "body": "Bad Request"
            }
        
        # Delete the item from DynamoDB
        table.delete_item(
            Key={"accountID": account_id}
        )

        # List and delete all files with the prefix `accountID.`
        existing_objects = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=f"{account_id}."
        )
        
        if 'Contents' in existing_objects:
            for obj in existing_objects['Contents']:
                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=obj['Key']
                )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": "OK"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": "Internal Server Error"
        }
