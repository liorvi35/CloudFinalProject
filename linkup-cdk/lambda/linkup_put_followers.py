import boto3

dynamodb = boto3.resource("dynamodb")

followers_table = dynamodb.Table("linkup-followers")


def update_attribute(account_id, attribute, new_value):
    followers_table.update_item(
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
            # goal: remove src from dst's `followers` and remove dst from src's `following`
            src_account_id = event["srcAccountID"]
            dst_account_id = event["dstAccountID"]
        except KeyError as e:
            print(str(e))
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        try:
            src_item = followers_table.get_item(Key={"accountID": src_account_id})
            src_following = list(src_item["Item"]["following"])
            if dst_account_id not in src_following:
                raise KeyError("Not Found")
                
            src_following.remove(dst_account_id)
            update_attribute(src_account_id, "following", src_following)
            
            dst_item = followers_table.get_item(Key={"accountID": dst_account_id})
            dst_followers = list(dst_item["Item"]["followers"])
            if src_account_id in dst_followers:
                raise KeyError("Not Found")
                
            dst_followers.remove(src_account_id)
            update_attribute(dst_account_id, "followers", dst_followers)
        except KeyError as e:
            print(str(e))
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
