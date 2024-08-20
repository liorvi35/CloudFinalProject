import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export class LinkupCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const labRole = iam.Role.fromRoleArn(this, 'Role', "arn:aws:iam::991888206011:role/LabRole", { mutable: false });
	
	// S3 bucket for user's profile picture
    const linkup_profile_pictures = new s3.Bucket(this, 'linkup_profile_pictures', {
      bucketName: 'linkup-profile-pictures',
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    });
    linkup_profile_pictures.grantReadWrite(labRole);
	
	// S3 bucket for holding post's images
	const linkup_post_pictures = new s3.Bucket(this, 'linkup_post_pictures', {
      bucketName: 'linkup-post-pictures',
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    });
    linkup_post_pictures.grantReadWrite(labRole);
	
	// DynamoDB table for holding users
	const linkup_users = new dynamodb.Table(this, 'linkup_users', {
      tableName: 'linkup-users',
      partitionKey: { name: 'accountID', type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      billingMode: dynamodb.BillingMode.PROVISIONED,
      readCapacity: 1,
      writeCapacity: 1,
    });
    linkup_users.addGlobalSecondaryIndex({
      indexName: 'email',
      partitionKey: { name: 'email', type: dynamodb.AttributeType.STRING },
      projectionType: dynamodb.ProjectionType.ALL,
      readCapacity: 1,
      writeCapacity: 1,
    });
	linkup_users.grantFullAccess(labRole);

  // DynamoDB table for holding posts
    const linkup_posts = new dynamodb.Table(this, 'linkup_posts', {
      tableName: 'linkup-posts',
      partitionKey: { name: 'accountID', type: dynamodb.AttributeType.STRING },
      sortKey: {name:'postTime', type: dynamodb.AttributeType.STRING},
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      billingMode: dynamodb.BillingMode.PROVISIONED,
      readCapacity: 1,
      writeCapacity: 1,
    });
    linkup_posts.grantFullAccess(labRole);

  // DynamoDB table for holding "followers"
  const linkup_followers = new dynamodb.Table(this, 'linkup_followers', {
    tableName: 'linkup-followers',
    partitionKey: { name: 'accountID', type: dynamodb.AttributeType.STRING },
    removalPolicy: cdk.RemovalPolicy.DESTROY,
    billingMode: dynamodb.BillingMode.PROVISIONED,
    readCapacity: 1,
    writeCapacity: 1,
  });
  linkup_followers.grantFullAccess(labRole);

  //lambda...
  const index = new lambda.Function(this, 'linkup-get-index', {
    runtime: lambda.Runtime.PYTHON_3_12,
    code: lambda.Code.fromAsset('lambda'),
    handler: 'index.lambda_handler',
    role: labRole,
  });

  //linkup api gateway
  const linkup_api_gateway = new apigateway.RestApi(this, 'linkup_api_gateway', {
    endpointTypes: [apigateway.EndpointType.REGIONAL],
    restApiName: 'linkup-api-gateway',
    description: 'linkUp social Network.', 
  });

  const index_resource = linkup_api_gateway.root.addResource('index');
  index_resource.addMethod('GET', new apigateway.LambdaIntegration(index));

  new cdk.CfnOutput(this, 'API Endpoint', {
    value: linkup_api_gateway.url,
  });

  }
}
