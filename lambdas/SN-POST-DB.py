import json
import boto3
from boto3.dynamodb.conditions import Key

DYNAMO_DB_SERVICE = "dynamodb"
TABLE_NAME = "SN-Users"

S3_SERVICE = "s3"
BUCKET_NAME = "sn-profile-pictures"
TIMEOUT = 3600

DEFAULT_PICTURE_KEY_FEMALE = "female_default.png"
DEFAULT_PICTURE_KEY_MALE = "male_default.png"

def lambda_handler(event, context):
    try:
        try:
            account_id = event["accountID"]
            first_name = event["firstName"]
            last_name = event["lastName"]
            email = event["email"]
            hash_password = event["hashPassword"]
            birth_date = event["birthDate"]
            gender = event["gender"]
        except KeyError:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "body": "Bad Request"
            }

        dynamodb = boto3.resource(DYNAMO_DB_SERVICE)
        table = dynamodb.Table(TABLE_NAME)

        check_existing = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        if int(check_existing["Count"]) != 0:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "body": "Bad Request"
            }

        s3_client = boto3.client(S3_SERVICE)
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": DEFAULT_PICTURE_KEY_MALE if gender == "male" else DEFAULT_PICTURE_KEY_FEMALE
            },
            ExpiresIn=TIMEOUT
        )

        user_details = {
            "accountID": account_id,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "hashPassword": hash_password,
            "birthDate": birth_date,
            "gender": gender,
            "profilePicture": presigned_url
        }

        # Insert new user into DynamoDB
        insert_new_user = table.put_item(Item=user_details)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": "OK",
            "profilePicture": presigned_url
        }
    except Exception:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": "Internal Server Error"
        }
