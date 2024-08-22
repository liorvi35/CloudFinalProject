import boto3


dynamodb = boto3.resource("dynamodb")

users_table = dynamodb.Table("linkup-users")

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