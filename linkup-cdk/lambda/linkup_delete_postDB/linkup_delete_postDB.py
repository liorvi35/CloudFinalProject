import boto3

dynamodb = boto3.resource("dynamodb")

posts_table = dynamodb.Table("linkup-posts")

s3 = boto3.client("s3")

posts_bucket = "linkup-post-pictures"


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
        
        response = posts_table.get_item(
            Key={
                "accountID": post_account_id,
                "postTime": post_time
            }
        )

        url_s3 = response["Item"]["postPicture"]

        file_name = (url_s3.split("?")[0]).split(".com/")[1]

        posts_table.delete_item(
            Key={
                "accountID": post_account_id,
                "postTime": post_time
            }
        )

        s3.delete_object(Bucket=posts_bucket, Key=file_name)

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