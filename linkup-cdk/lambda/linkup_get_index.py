def lambda_handler(event, context):
    return {
        'statusCode': 200,
		'headers': {
			'Content-Type': 'text/html'
		},
        'body': "<!DOCTYPE html><html><body><h1>LinkUp</h1></body></html>"
    }