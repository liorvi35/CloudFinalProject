import boto3
import base64
import json


dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")

s3 = boto3.client("s3")

profile_pictures_bucket = "linkup-profile-pictures"


def update_attribute(account_id, attribute, new_value):
    users_table.update_item(
        Key={"accountID": account_id},
        UpdateExpression=f"set {attribute} = :e",
        ExpressionAttributeValues={
            ":e": new_value
        },
        ReturnValues="UPDATED_NEW"
    )


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
        
        is_picture = False
        try:
            base_64_file = event["base64File"]
            format = event["format"]
            is_picture = True
        except KeyError:
            pass

        if is_picture:
            image_data = base64.b64decode(base_64_file)
            new_object_key = f"{account_id}.{format}"

            s3.put_object(
                Bucket=profile_pictures_bucket,
                Key=new_object_key,
                Body=image_data,
                ContentType=f"image/{format}"
            )

            profile_picture_signed = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": profile_pictures_bucket, "Key": new_object_key},
                ExpiresIn=604800
            )

            update_attribute(account_id, "profilePicture", profile_picture_signed)

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({ "message": "OK", "profilePicture": profile_picture_signed})
            }

        else:
            count = 0
            try:
                for attribute in ["firstName", "lastName", "hashedPassword", "email", "birthDate", "gender"]:
                    value = event.get(attribute)
                    if value:
                        update_attribute(account_id, attribute, value)
                        count += 1
            except KeyError:
                pass

            if count == 0:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": "Bad Request"
                }
        
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