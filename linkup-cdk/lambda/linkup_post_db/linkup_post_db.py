import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")
followers_table = dynamodb.Table("linkup-followers")

s3 = boto3.client("s3")
profile_pictures_bucket = "linkup-profile-pictures"

female_default_picture = "female_default.png"
male_default_picture = "male_default.png"


def lambda_handler(event, context):
    try:
        # Extract user details from event
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
            print(f"Key {str(e)} does not exist")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request: Missing required fields"
            }
        
        # Check if any of the required fields are empty
        for key, value in new_user_item.items():
            if value == "" or value is None:
                print(f"Empty field: {key}")
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": f"Bad Request: {key} cannot be empty"
                }

        # Check if accountID already exists
        check_account_id_exists_users = users_table.get_item(Key={"accountID": new_user_item["accountID"]})
        if "Item" in check_account_id_exists_users:
            print("accountID already exists")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request: accountID already exists"
            }

        # Check if email already exists
        check_email_exists_users = users_table.query(
            IndexName="email",
            KeyConditionExpression=Key("email").eq(new_user_item["email"])
        )
        if int(check_email_exists_users["Count"]) > 0:
            print("email already exists")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request: email already exists"
            }
        
        # Generate the profile picture URL
        profile_picture_signed = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": profile_pictures_bucket, "Key": female_default_picture if new_user_item["gender"] == "female" else male_default_picture},
            ExpiresIn=604800
        )

        new_user_item["profilePicture"] = profile_picture_signed

        # Save the user and follower items to DynamoDB
        users_table.put_item(Item=new_user_item)
        followers_table.put_item(Item=new_follower_item)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "OK", "profilePicture": profile_picture_signed})
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
