import boto3
from boto3.dynamodb.conditions import Key
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("linkup-posts")

def lambda_handler(event, context):
    try:
        response = table.scan()
        print(response)

        posts = response["Items"]

        posts.sort(key=lambda x: int(x['postTime']))

        posts.reverse()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(posts)
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
