import boto3


dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")

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
