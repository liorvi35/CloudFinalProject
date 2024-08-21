import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")

followers_table = dynamodb.Table("linkup-followers")


def lambda_handler(event, context):
    try:
        try:
            new_user_item = {
                "accountID": event["accountID"],
                "firstName": event["firstName"],
                "lastName": event["lastName"],
                "hashedPassword": event["hashedPassword"],
                "email": event["email"],
                "birthDate": event["birthDate"],
                "gender": event["gender"]
            }

            new_follower_item = {
                "accountID": event["accountID"],
                "followers": [],
                "following": []
            }
        except KeyError as e:
            print(f"Key {str(e)} does not exists")
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Not Found"
            }
        
        check_account_id_exists_users = users_table.get_item(Key={"accountID": new_user_item["accountID"]})

        check_email_exists_users = users_table.query(IndexName="email", KeyConditionExpression=Key("email").eq(new_user_item["email"]))

        check_account_id_exists_followers = followers_table.get_item(Key={"accountID": new_user_item["accountID"]})

        if "Item" in check_account_id_exists_users or int(check_email_exists_users["Count"]) > 0 or "Item" in check_account_id_exists_followers:
            print("accountID or email already exists")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        users_table.put_item(Item=new_user_item)

        followers_table.put_item(Item=new_follower_item)
        
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
