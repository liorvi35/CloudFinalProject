import boto3
from boto3.dynamodb.conditions import Key
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("linkup-followers")


def lambda_handler(event, context):
    try:
        try:
            account_id = event["queryStringParameters"]["accountID"]
        except KeyError:
            return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Bad Request"
        }

        response = table.get_item(Key={"accountID": account_id})

        item = response.get("Item")
        if not item:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Not Found"
            }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(item)
        }

    except Exception as e:
        print(str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Internal Server Error"
        }
