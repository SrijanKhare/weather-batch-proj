import boto3

def invoke_lambda_func(function_name: str):

	lambda_client = boto3.client('lambda')

	response = lambda_client.invoke(function_name)

	if response['StatusCode'] != 200:
		print('error')
	




