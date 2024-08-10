import json
import boto3
from boto3.dynamodb.conditions import Key

DYNAMO_DB_SERVICE = "dynamodb"
TABLE_NAME = "SN-Users"

def lambda_handler(event, context):
    try:
        try:
            email = event["email"]
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
        
        check_existing = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        if int(check_existing["Count"]) == 0:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "body": "Bad Request"
            }
            
        user_details = {
            "accountID": check_existing["Items"][0]["accountID"],
            "firstName": check_existing["Items"][0]["firstName"],
            "lastName": check_existing["Items"][0]["lastName"],
            "email": check_existing["Items"][0]["email"],
            "hashPassword": check_existing["Items"][0]["hashPassword"],
            "profilePicture": check_existing["Items"][0]["profilePicture"]
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(user_details)
        }
    except Exception:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": "Internal Server Error"
        }
