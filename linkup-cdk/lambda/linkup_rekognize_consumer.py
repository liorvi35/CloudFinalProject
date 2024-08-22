import base64
import boto3
import json
import urllib3


dynamodb = boto3.resource("dynamodb")

posts_table = dynamodb.Table("linkup-posts")

rekognition = boto3.client("rekognition")

http = urllib3.PoolManager()



def lambda_handler(event, context):
    try:
        try:
            body = event["Records"][0]["body"]
            
            print(body)
            
            signed_url = body.split(";")[0]
            
            account_id = ((body.split(";")[1]).split(".")[0]).split("_")[0]
            
            post_time = ((body.split(";")[1]).split(".")[0]).split("_")[1]
            
            print("account_id = ", account_id)
            
            print("postTime = ", post_time)
            
            response = http.request("GET", signed_url)
        
            if response.status != 200:
                return {
                    "statusCode": response.status,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": response.status
                }
            
            image_bytes = response.data
            
            rekognition_response = rekognition.detect_labels(
                Image={
                    "Bytes": image_bytes
                    
                },
                MaxLabels=10,
                MinConfidence=75
            )
            
            labels = rekognition_response.get("Labels", [])
            unique_labels = [label["Name"] for label in labels]
            
            print(unique_labels)
            
            response = posts_table.update_item(
                Key={
                    'accountID': account_id,
                    'postTime': post_time
                    
                },
                UpdateExpression="set #x_attr = :x_val",
                ExpressionAttributeNames={'#x_attr': 'pictureTags'},
                ExpressionAttributeValues={':x_val': unique_labels},
                ReturnValues="UPDATED_NEW"
            )
            
            print("response = ", response)
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "OK"
            }

        except KeyError as e:
            return {
                "statusCode": 400, 
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
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
