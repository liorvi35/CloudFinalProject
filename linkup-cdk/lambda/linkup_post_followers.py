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
            # goal: add src to dst's `followers` and add dst to src's `following`
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

        src_item = followers_table.get_item(Key={"accountID": src_account_id})
        src_following = list(src_item["Item"]["following"])
        if dst_account_id in src_following:
            return {
                "statusCode": 409,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Conflict"
            }
        src_following.append(dst_account_id)
        update_attribute(src_account_id, "following", src_following)
        
        dst_item = followers_table.get_item(Key={"accountID": dst_account_id})
        dst_followers = list(src_item["Item"]["followers"])
        if src_account_id in dst_followers:
            return {
                "statusCode": 409,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Conflict"
            }
        dst_followers.append(src_account_id)
        update_attribute(dst_account_id, "followers", dst_followers)
        
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
