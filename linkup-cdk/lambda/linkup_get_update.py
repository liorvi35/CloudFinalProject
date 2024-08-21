def lambda_handler(event, context):
    return {
        'statusCode': 200,
		'headers': {
			'Content-Type': 'application/json'
		},
        'body': "<!DOCTYPE html><html><body><h1>GET /update HTTP</h1></body></html>"
    }