import boto3


dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")

posts_table = dynamodb.Table("linkup-posts")

followers_table = dynamodb.Table("linkup-followers")


def lambda_handler(event, context):
    try:
        try:
            account_id = event["accountID"]
        except KeyError as e:
            print(f"Key {str(e)} does not exists")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        users_table.delete_item(Key={"accountID": account_id})

        followers_table.delete_item(Key={"accountID": account_id})

        response = posts_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("accountID").eq(account_id)
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
