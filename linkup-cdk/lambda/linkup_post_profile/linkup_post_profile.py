def lambda_handler(event, context):
    return {
        'statusCode': 200,
		'headers': {
			'Content-Type': 'application/json'
		},
        'body': "<!DOCTYPE html><html><body><h1>POST /profile HTTP</h1></body></html>"
    }