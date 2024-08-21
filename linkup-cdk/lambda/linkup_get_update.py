def lambda_handler(event, context):
    try:
        with open("pages/update.html") as f:
            page_contents = f.read()
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": page_contents
        }
    except:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": "<h1>Internal Server Error</h1>"
        }
