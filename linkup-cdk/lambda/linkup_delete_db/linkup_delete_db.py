import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")
posts_table = dynamodb.Table("linkup-posts")
followers_table = dynamodb.Table("linkup-followers")


def lambda_handler(event, context):
    try:
        # Extract the accountID from the event
        try:
            account_id = event["accountID"]
        except KeyError as e:
            print(f"Key {str(e)} does not exist")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        # Check if the user exists in the users_table
        user_response = users_table.get_item(Key={"accountID": account_id})

        if "Item" not in user_response:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "User not found"
            }

        # Proceed to delete the user, followers, and posts
        users_table.delete_item(Key={"accountID": account_id})
        followers_table.delete_item(Key={"accountID": account_id})

        # Retrieve and delete posts
        response = posts_table.query(
            KeyConditionExpression=Key("accountID").eq(account_id)
        )

        for item in response.get("Items", []):
            posts_table.delete_item(
                Key={
                    "accountID": item["accountID"],
                    "postTime": item["postTime"]
                }
            )
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "OK"
        }

    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Internal Server Error"
        }
