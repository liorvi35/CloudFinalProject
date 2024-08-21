import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("linkup-users")


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
        except KeyError as e:
            print(str(e))
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        check_account_id_exists = table.get_item(Key={"accountID": new_user_item["accountID"]})
        if "Item" in check_account_id_exists:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        check_email_exists = table.query(IndexName="email", KeyConditionExpression=Key("email").eq(new_user_item["email"]))
        if int(check_email_exists["Count"]) > 0:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        table.put_item(Item=new_user_item)
        
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
