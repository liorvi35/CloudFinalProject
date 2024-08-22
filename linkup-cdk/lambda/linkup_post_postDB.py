import boto3
import base64
import json

dynamodb = boto3.resource("dynamodb")

posts_table = dynamodb.Table("linkup-posts")

s3 = boto3.client("s3")

posts_pictures_bucket = "linkup-post-pictures"


def lambda_handler(event, context):
    try:
        try:
            account_id = event["accountID"]
            post_time = event["postTime"]
        except KeyError as e:
            print(f"Key {str(e)} does not exists")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request1"
            }

        is_text = False
        is_picture = False
        is_format = False

        post_text = event.get("postText")
        post_picture_base64 = event.get("postPicture")
        picture_format = event.get("format")

        if post_text:
            is_text = True
        if post_picture_base64:
            is_picture = True
        if picture_format:
            is_format = True

        if (not is_text and not is_picture) or (is_picture and not is_format) or (is_format and not is_picture):
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request2"
            }

        if is_picture:
            image_data = base64.b64decode(post_picture_base64)
            new_object_key = f"{account_id}_{post_time}.{picture_format}"

            s3.put_object(
                Bucket=posts_pictures_bucket,
                Key=new_object_key,
                Body=image_data,
                ContentType=f"image/{picture_format}"
            )

            picture_sigend_url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": posts_pictures_bucket, "Key": new_object_key},
                ExpiresIn=604800
            )

            post_item = {
                "accountID": account_id,
                "postTime": str(post_time),
                "postPicture": picture_sigend_url,
                "postText": None,
                "pictureTags": []
            }

            if is_text:
                post_item["postText"] = post_text

        else:
            post_item = {
                "accountID": account_id,
                "postTime": str(post_time),
                "postPicture": None,
                "postText": post_text,
                "pictureTags": []
            }

        posts_table.put_item(Item=post_item)

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