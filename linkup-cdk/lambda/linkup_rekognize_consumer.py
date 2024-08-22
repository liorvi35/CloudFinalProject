"""
{
    'Records': [
        {
            'messageId': '862b6a9d-ad49-4db9-8269-116d3cfd54ec',
            'receiptHandle': 'AQEBjPijHsHf6PVRwo+g09CwZjN32xlnsh080JafmrQ1upEYIaVKONqXLI7/6kTcmSDl79JcOLyYkGy2jFu2+bH+LuD6htXjHErN+HXeOpKSdAQvzP7S/+67n+hG8tNJIrF8shwgXKiJymsgP/2ms05IDZVW5UGzjzgAx/H+gK+Km9iFA+2lWMKmEtE/YcGsKEHfjlj25sKfC+Z220L2hs4DPCzHB8OlCnSbwWVpoYb+49nijHl8CB0LQwvJIazI1ZTkN2KOtrPA4y6cuSnQpw/MGkrnhIsUr2l4QwGzkSCvhKKiyahi17F5gpi6Y+yDk0xVfbHdr4iKlxyAYStEWjJMBkwl0EFz/IqDLVwtgsUG+2RMxvnIwMm0XgGRCPx6w/z1',
            'body': '
            
https://linkup-post-pictures.s3.amazonaws.com/48ba4aac-aed0-cf00-de29-45be374484e3_1724342915.jpeg?AWSAccessKeyId=ASIA5EV3AJGWI5OVXOZF&Signature=zeSbAOwFaST0vDYDSawLljU67Tc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCxwS39aoAJ3jcL8ydFL0M%2BhbU6Yb1SwW99ec2LInwsXAIgI%2FIOnFRtFc%2Bqo4t8MnRMeBnKqr2CzLuhMjVCLqjQKgYqxgMIkf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw5MDM0MDkwNjAyNjgiDDAVsSbTanfmOAdJNCqaA1t7dRF6svvZZta1Qy%2BBAGg06z2AdrSvl1G6zWHB52r6odjdKCmaLt6UdSA7a3JS4Ob3KhuspZgIZHYfg6MIXw3MX05IBcSkiAHQwtxi37kAzxZBgO79zNmEZIwX64t7utbZPW5F6pk5JF1PxgLhgL2X4nZ2ItBmDyUGSyuFDJf%2Bk7s%2FkOXVIZrUKaG%2BNAB0OqdvWn8%2BqgKI3Kt6EZ9h0nBbFgDTAQ%2BYAmorcRD3E%2FMwKFOSh9KGl3JfhF3ZEpnLeKqXcdTsFIli9X1O4VFVN9gYtA23sUAcD52Wk0JKjDGPTE19lUVONubn30cqxO%2Bving5g5K%2BDBDjtvGvnz6k7QmRMzAkxbtFJ5B23n5tiQHjjvTK333g%2Buf5gr2avBAOuo5jVG7aK9sAOwfArDeeVXEWdkIFOOJtPwFy%2BBIvt10oIp%2FHmCxoy5mYuCWMPxtXrvePne9Cwy9MEpq2JjIPHlHJxeURD5fycE10HXUk4Yrqn5%2F3kxLgGaevUVfmlpX7I5nqsA%2B7BtRazCsIfXqb0zXRYTrtRK%2F7f2NjMIPFnbYGOp4BELKMs9e3eFuKgeWaCJ6zJBenNBm2cGXwlldn063WoJ9X9ge0DBCqg9NOovLQiln%2FlzE5VShZCT%2F7FE2%2FHP20rpL5wYrWI0EqW7dkyNvcbPLLDF1dPgNhPDAJmpXHn00LZhUwuQXKK7sK6kPPAyLlv3ZSyS6RCChzCwObyWmxw6LL44op7Fgpen2cmEQBX0OICyS92piO9kpg97IKLR8%3D&Expires=1724947717
            
            ',
            'attributes': {
                'ApproximateReceiveCount': '1',
                'SentTimestamp': '1724342949484',
                'SenderId': 'AROA5EV3AJGWEUYRBHFY6:user3439242=Levi_man',
                'ApproximateFirstReceiveTimestamp': '1724343227074'
            },
            'messageAttributes': {},
            'md5OfBody': 'd70a7b8280fbfe806e7f700f9f50745c',
            'eventSource': 'aws:sqs',
            'eventSourceARN': 'arn:aws:sqs:us-east-1:903409060268:rekognize',
            'awsRegion': 'us-east-1'
            
        }
    ]
}
"""

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
