import json
import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")


def lambda_handler(event, context):
    try:
        try:
            email = event["queryStringParameters"]["email"]
            hashed_password = event["queryStringParameters"]["hashedPassword"]
            print(email)
            print(hashed_password)
        except KeyError as e:
            print(f"Key {str(e)} does not exists")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }
        
        check_email_exists_users = users_table.query(IndexName="email", KeyConditionExpression=Key("email").eq(email))
        
        print(check_email_exists_users["Items"][0])
        
        if hashed_password == check_email_exists_users["Items"][0]["hashedPassword"]:
            existing_user_item = {
                "accountID": check_email_exists_users["Items"][0]["accountID"],
                "firstName": check_email_exists_users["Items"][0]["firstName"],
                "lastName": check_email_exists_users["Items"][0]["lastName"],
                "email": check_email_exists_users["Items"][0]["email"],
                "birthDate": check_email_exists_users["Items"][0]["birthDate"],
                "gender": check_email_exists_users["Items"][0]["gender"]
            }

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(existing_user_item)
            }

        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Not Found"
        }

    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Internal Server Error11"
        }
