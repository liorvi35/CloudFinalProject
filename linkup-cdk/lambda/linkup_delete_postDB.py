import boto3

dynamodb = boto3.resource("dynamodb")

posts_table = dynamodb.Table("linkup-posts")


def lambda_handler(event, context):
    try:
        try:
            post_account_id = event["postAccountID"]
            post_time = event["postTime"]
        except KeyError as e:
            print(str(e))
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }
        
        response = posts_table.delete_item(
            Key={
                "accountID": post_account_id,
                "postTime": post_time
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
        print(str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Internal Server Error"
        }