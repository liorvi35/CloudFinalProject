from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_apigateway as api_gateway,
    aws_lambda as lambda,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    core
)


class SnStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "sn-profile-pictures-2")