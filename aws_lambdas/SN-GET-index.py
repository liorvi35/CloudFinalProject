import json

REGISTER_PAGE = "index.html"

def lambda_handler(event, context):
    with open(REGISTER_PAGE, "r") as f:
        register_page = f.read()
    
    return register_page
