import boto3
from openai import AzureOpenAI
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone
import time


# credentials for SMTP server
(USERNAME, PASSWORD) = ("564c21001@smtp-brevo.com", "dPZbwv2tnGUyQ4E7")

# address of SMTP server
(SERVER, PORT) = ("smtp-relay.brevo.com", 587)


dynamodb = boto3.resource("dynamodb")
users_table = dynamodb.Table("linkup-users")
followers_table = dynamodb.Table("linkup-followers")
posts_table = dynamodb.Table("linkup-posts")


def ask_gpt(post, deployment_name="prod"):
    client = AzureOpenAI(
        api_key="ffeab3c02a40418ba5fc5ad00fac007a",
        api_version="2024-02-01",
        azure_endpoint="https://linkup-openai.openai.azure.com/"
    )

    response = client.completions.create(
        model=deployment_name,
        prompt=f"describe this post: posted: \"{post}\". describe shortly.",
        temperature=0.2,
        max_tokens=((len(post) + len("describe this post: Meni Samet posted: \"\". describe shortly.")) // 4) + 100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1,
        stop=None
    )

    return response.choices[0].text


def send_email(sender_email: str,
               sender_name: str,
               receiver_email: str,
               receiver_name: str,
               subject: str,
               content: str) -> None:
    message = MIMEMultipart()
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = f"{receiver_name} <{receiver_email}>"
    message["Subject"] = subject
    message.attach(MIMEText(content, "plain"))
    with smtplib.SMTP(SERVER, PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, receiver_email, message.as_string())
        server.quit()


def convert_epoch_to_israel_time(epoch_timestamp):
    israel_tz = timezone(timedelta(hours=3))
    utc_dt = datetime.fromtimestamp(epoch_timestamp, tz=timezone.utc)
    israel_dt = utc_dt.astimezone(israel_tz)
    formatted_date = israel_dt.strftime('%d/%m/%Y, %H:%M:%S')
    return formatted_date


def lambda_handler(event, context):
    try:
        try:
            account_id = event["accountID"]
        except KeyError as e:
            print(str(e))
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Bad Request"
            }
        
        response = users_table.get_item(Key={"accountID": account_id})
        if not response["Item"]:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Not Found"
            }    
        user_item = response["Item"]

        # 2. get posts by following's ids

        response = followers_table.get_item(Key={"accountID": account_id})
        if not response["Item"]:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Not Found"
            }
        followings = list(response["Item"]["following"])


        friends_posts = []
        for following in followings:
            response = posts_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key("accountID").eq(following)
            )
            if int(response["Count"]) <= 0:
                continue
            for item in response["Items"]:
                if (int(time.time()) - int(item["postTime"])) > 86400:
                    continue
                friends_posts.append(item)

        friends_posts = sorted(friends_posts, key=lambda x: int(x["postTime"]))
        friends_posts.reverse()

        contents = f"<!DOCTYPE html><html><body><h1>Hi, {user_item["firstName"]} {user_item["lastName"]}!</h1><h2>Here is the TL;DR for your friends feed:</h2><div>"

        for post, i in zip(friends_posts, range(len(friends_posts))):
            response = users_table.get_item(Key={"accountID": post["accountID"]})
            if not response["Item"]:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": "Not Found"
                }
            poster_details = response["Item"]
            post_summery = f"<div><p>{i + 1}. {poster_details["firstName"]} {poster_details["lastName"]}: {ask_gpt(post["postText"]).replace("\n", "")} posted on: {convert_epoch_to_israel_time(int(post["postTime"]))}.</p></div><br/>"
            contents += post_summery

        contents += "</div><p>Best Regards,</p><br/><h4>LinkUp</h4></body></html>"

        print(contents)
        
        send_email("auto@linkup.aws",
                   "LinkUp Auto Sender",
                   f"{user_item["email"]}",
                   f'{user_item["firstName"]} {user_item["lastName"]}',
                   "LinkUp - TL;DR",
                   contents)

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
