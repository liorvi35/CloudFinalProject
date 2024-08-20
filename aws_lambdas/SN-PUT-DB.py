import json
import boto3
import base64

DYNAMO_DB_SERVICE = "dynamodb"
S3_SERVICE = "s3"
TABLE_NAME = "SN-Users"
BUCKET_NAME = "sn-profile-pictures"

def lambda_handler(event, context):
    try:
        account_id = event["accountID"]
        profile_picture_b64 = event["profilePicture"]
        format = event["format"]
        
        # Decode the base64-encoded image
        profile_picture_data = base64.b64decode(profile_picture_b64)

        s3_client = boto3.client(S3_SERVICE)
        
        # Delete any existing objects with the same accountID, regardless of the extension
        existing_objects = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=f"{account_id}."
        )

        if 'Contents' in existing_objects:
            for obj in existing_objects['Contents']:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])

        # Define the S3 object key using accountID and format
        object_key = f"{account_id}.{format}"

        # Upload the profile picture to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
            Body=profile_picture_data,
            ContentType=f"image/{format}"
        )

        # Generate a pre-signed URL for the uploaded object
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': object_key
            },
            ExpiresIn=3600
        )

        # Update the DynamoDB table with the new profile picture URL
        dynamodb = boto3.resource(DYNAMO_DB_SERVICE)
        table = dynamodb.Table(TABLE_NAME)
        
        table.update_item(
            Key={
                'accountID': account_id
            },
            UpdateExpression="SET profilePicture = :url",
            ExpressionAttributeValues={
                ':url': presigned_url
            }
        )

        # Return the pre-signed URL in the response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"presignedUrl": presigned_url})
        }
    
    except Exception as e:
        print("Error occurred:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Internal Server Error"})
        }
