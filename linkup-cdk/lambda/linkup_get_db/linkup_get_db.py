import json
import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")


def lambda_handler(event, context):
    try:
        is_uuid = False
        try:
            try:
                account_id = event["queryStringParameters"]["accountID"]
                is_uuid = True
            except KeyError:
                email = event["queryStringParameters"]["email"]
                hashed_password = event["queryStringParameters"]["hashedPassword"]
        except KeyError as e:
            print(f"Key {str(e)} does not exists")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }
        
        if not is_uuid:
            check_email_exists_users = users_table.query(IndexName="email", KeyConditionExpression=Key("email").eq(email))

            if int(check_email_exists_users["Count"]) == 1 and hashed_password == check_email_exists_users["Items"][0]["hashedPassword"]:
                existing_user_item = {
                    "accountID": check_email_exists_users["Items"][0]["accountID"],
                    "firstName": check_email_exists_users["Items"][0]["firstName"],
                    "lastName": check_email_exists_users["Items"][0]["lastName"],
                    "email": check_email_exists_users["Items"][0]["email"],
                    "birthDate": check_email_exists_users["Items"][0]["birthDate"],
                    "gender": check_email_exists_users["Items"][0]["gender"],
                    "profilePicture": check_email_exists_users["Items"][0]["profilePicture"]
                }

            else:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": "Not Found"
                }
            
        else:
            if account_id == "ALL":
                all_users = users_table.scan()
                users = all_users["Items"] if all_users["Count"] > 0 else []
                users = [{k: v for k, v in d.items() if k != "hashedPassword"} for d in users]
                existing_user_item = users
                
            else:   
                check_account_id_exists_users = users_table.get_item(Key={"accountID": account_id})

                if "Item" in check_account_id_exists_users:
                    existing_user_item = {
                        "accountID": check_account_id_exists_users["Item"]["accountID"],
                        "firstName": check_account_id_exists_users["Item"]["firstName"],
                        "lastName": check_account_id_exists_users["Item"]["lastName"],
                        "email": check_account_id_exists_users["Item"]["email"],
                        "birthDate": check_account_id_exists_users["Item"]["birthDate"],
                        "gender": check_account_id_exists_users["Item"]["gender"],
                        "profilePicture": check_account_id_exists_users["Item"]["profilePicture"]
                    }
                    
                else:
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
            "body": json.dumps(existing_user_item)
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
