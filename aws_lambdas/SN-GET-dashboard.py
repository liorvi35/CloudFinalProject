import json

REGISTER_PAGE = "dashboard.html"

def lambda_handler(event, context):
    with open(REGISTER_PAGE, "r") as f:
        dashboard_page = f.read()
    
    return dashboard_page
