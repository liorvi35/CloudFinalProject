import boto3

dynamodb = boto3.resource("dynamodb")
posts_table = dynamodb.Table("linkup-posts")

def lambda_handler(event, context):
    try:
        try:
            post_account_id = event["postAccountID"]
            post_time = event["postTime"]
            liker_account_id = event["likerAccountID"]
        except KeyError as e:
            print(str(e))
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        is_like = event.get("isLike")
        comment_text = event.get("commentText")
        comment_time = str(event.get("commentTime"))

        if not (is_like or (comment_text and comment_time)) or (is_like and (comment_text or comment_time)):
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }

        post_item = posts_table.get_item(
            Key={
                "accountID": post_account_id,
                "postTime": post_time
            }
        )

        post = post_item.get("Item")
        
        if not post:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Not Found"
            }

        # Handling likes
        if is_like is not None:
            likes = post.get("likes", [])

            if is_like:
                if liker_account_id in likes:
                    return {
                        "statusCode": 409,
                        "headers": {
                            "Content-Type": "application/json"
                        },
                        "body": "Conflict"
                    }
                likes.append(liker_account_id)
            else:
                if liker_account_id not in likes:
                    return {
                        "statusCode": 409,
                        "headers": {
                            "Content-Type": "application/json"
                        },
                        "body": "Conflict"
                    }
                likes.remove(liker_account_id)

            posts_table.update_item(
                Key={
                    "accountID": post_account_id,
                    "postTime": post_time
                },
                UpdateExpression="SET likes = :newLikes",
                ExpressionAttributeValues={
                    ":newLikes": likes
                },
                ReturnValues="UPDATED_NEW"
            )

        else:
            comments = post.get("comments", [])
            new_comment = {liker_account_id: {comment_time: comment_text}}

            user_comments = next((comment for comment in comments if liker_account_id in comment), None)
            if user_comments:
                if comment_time in user_comments[liker_account_id]:
                    return {
                        "statusCode": 409,
                        "headers": {
                            "Content-Type": "application/json"
                        },
                        "body": "Conflict"
                    }
                user_comments[liker_account_id].update(new_comment[liker_account_id])
            else:
                comments.append(new_comment)

            posts_table.update_item(
                Key={
                    "accountID": post_account_id,
                    "postTime": post_time
                },
                UpdateExpression="SET comments = :newComments",
                ExpressionAttributeValues={
                    ":newComments": comments
                },
                ReturnValues="UPDATED_NEW"
            )

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
