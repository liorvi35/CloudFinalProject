import boto3
from openai import AzureOpenAI
import re

dynamodb = boto3.resource("dynamodb")
posts_table = dynamodb.Table("linkup-posts")


def ask_gpt(prompt, deployment_name="prod"):
    client = AzureOpenAI(
        api_key="ffeab3c02a40418ba5fc5ad00fac007a",
        api_version="2024-02-01",
        azure_endpoint="https://linkup-openai.openai.azure.com/"
    )

    response = client.completions.create(
        model=deployment_name,
        prompt=f"Classify this sentence: {prompt} -  is it 'Positive', 'Neutral' or 'Negative'?",
        temperature=0.2,
        max_tokens=((len(prompt) + len("Classify this sentence:  -  is it 'Positive', 'Neutral' or 'Negative'?")) // 4) + 100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1,
        stop=None
    )

    return response.choices[0].text

def lambda_handler(event, context):
    try:
        # Extract necessary fields
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

        # Get parameters from the event
        is_like = event.get("isLike")
        comment_text = event.get("commentText")
        comment_time = event.get("commentTime")
        
        print(f"isLike: {is_like}, commentText: {comment_text}, commentTime: {comment_time}")

        # Validate input based on the new conditions
        if (is_like is not None and comment_text is None and comment_time is None) or \
           (is_like is None and comment_text is not None and comment_time is not None):
            pass
        else:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request1"
            }

        # Retrieve the post item from DynamoDB
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
            comment_time = str(comment_time)
            comments = post.get("comments", [])

            classification = ask_gpt(comment_text)
            classification = classification.replace("\n", "")

            print(f"Classification of {comment_text} is {classification}")

            new_comment = {liker_account_id: {comment_time: [comment_text, classification]}}

            # Ensure that `comments` is a list of dictionaries
            updated_comments = []
            user_comments_updated = False

            for comment in comments:
                if liker_account_id in comment:
                    if comment_time in comment[liker_account_id]:
                        return {
                            "statusCode": 409,
                            "headers": {
                                "Content-Type": "application/json"
                            },
                            "body": "Conflict"
                        }
                    comment[liker_account_id][comment_time] = []
                    comment[liker_account_id][comment_time].append(comment_text)
                    comment[liker_account_id][comment_time].append(classification)
                    user_comments_updated = True
                updated_comments.append(comment)

            if not user_comments_updated:
                updated_comments.append(new_comment)

            posts_table.update_item(
                Key={
                    "accountID": post_account_id,
                    "postTime": post_time
                },
                UpdateExpression="SET comments = :newComments",
                ExpressionAttributeValues={
                    ":newComments": updated_comments
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
