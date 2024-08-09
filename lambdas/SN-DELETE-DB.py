import json
import boto3
from boto3.dynamodb.conditions import Key

DYNAMO_DB_SERVICE = "dynamodb"
TABLE_NAME = "SN-Users"

def lambda_handler(event, context):
    try:
        try:
            account_id = event["accountID"]
        except KeyError:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "body": "Bad Request"
            }

        dynamodb = boto3.resource(DYNAMO_DB_SERVICE)
        table = dynamodb.Table(TABLE_NAME)

        check_existing = table.get_item(
            Key={
                "accountID": account_id
            }
        )
        
        if not "Item" in check_existing.keys():
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "body": "Bad Request"
            }
        
        table.delete_item(
            Key={
                "accountID": account_id
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": "OK"
        }
    except Exception:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": "Internal Server Error"
        }
