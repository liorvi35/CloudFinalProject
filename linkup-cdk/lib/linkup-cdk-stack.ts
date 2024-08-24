import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { BucketDeployment, Source } from 'aws-cdk-lib/aws-s3-deployment';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as lambdaEventSources from 'aws-cdk-lib/aws-lambda-event-sources';



export class LinkupCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /* ---------- IAM ---------- */
    const labRole = iam.Role.fromRoleArn(this, "Role", "arn:aws:iam::903409060268:role/LabRole", { mutable: false });

    /* ---------- S3 ---------- */
	  // S3 bucket for user's profile picture
    const linkup_profile_pictures = this.createBucket("linkup-profile-pictures", labRole);
    this.deployObjectToS3("s3_def_profile_pics", "deployFemaleDefaultProfilePicture", linkup_profile_pictures, labRole);
    	
    // S3 bucket for holding post's images
    const linkup_post_pictures = this.createBucket("linkup-post-pictures", labRole);
    
    /* ---------- SQS ---------- */
    const rekognizeQueue = new sqs.Queue(this, 'rekognizeQueue', {
      queueName: 'linkup-rekognize-queue',
      visibilityTimeout: cdk.Duration.seconds(300)
    });
    const sqs_consumer = this.createLambda("linkup-rekognize-consumer", "lambda", "linkup_rekognize_consumer.lambda_handler", labRole);
    sqs_consumer.addEventSource(new lambdaEventSources.SqsEventSource(rekognizeQueue));


    /* ---------- DynamoDB ---------- */
	  // DynamoDB table for holding users
	  const linkup_users = new dynamodb.Table(this, "linkup_users", {
      tableName: "linkup-users",
      partitionKey: { name: "accountID", type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      billingMode: dynamodb.BillingMode.PROVISIONED,
      readCapacity: 1,
      writeCapacity: 1,
    });
    linkup_users.addGlobalSecondaryIndex({
      indexName: "email",
      partitionKey: { name: "email", type: dynamodb.AttributeType.STRING },
      projectionType: dynamodb.ProjectionType.ALL,
      readCapacity: 1,
      writeCapacity: 1,
    });
	  linkup_users.grantFullAccess(labRole);

    // DynamoDB table for holding posts
    const linkup_posts = new dynamodb.Table(this, "linkup_posts", {
      tableName: "linkup-posts",
      partitionKey: { name: "accountID", type: dynamodb.AttributeType.STRING },
      sortKey: { name:"postTime", type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      billingMode: dynamodb.BillingMode.PROVISIONED,
      readCapacity: 1,
      writeCapacity: 1,
    });
    linkup_posts.grantFullAccess(labRole);

    // DynamoDB table for holding "followers"
    const linkup_followers = new dynamodb.Table(this, "linkup_followers", {
      tableName: "linkup-followers",
      partitionKey: { name: "accountID", type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      billingMode: dynamodb.BillingMode.PROVISIONED,
      readCapacity: 1,
      writeCapacity: 1,
    });
    linkup_followers.grantFullAccess(labRole);

    /* ---------- Lambda ---------- */
    /* db */

    // POST /prod/db 
    const post_db = this.createLambda("linkup-post-db", "lambda", "linkup_post_db.lambda_handler", labRole);

    // GET /prod/db
    const get_db = this.createLambda("linkup-get-db", "lambda", "linkup_get_db.lambda_handler", labRole);

    // PUT /prod/db 
    const put_db = this.createLambda("linkup-put-db", "lambda", "linkup_put_db.lambda_handler", labRole);

    // DELETE /prod/db 
    const delete_db = this.createLambda("linkup-delete-db", "lambda", "linkup_delete_db.lambda_handler", labRole);

    /* followers */

    // POST /prod/followers 
    const post_followers = this.createLambda("linkup-post-followers", "lambda", "linkup_post_followers.lambda_handler", labRole);

    // GET /prod/followers 
    const get_followers = this.createLambda("linkup-get-followers", "lambda", "linkup_get_followers.lambda_handler", labRole);

    // PUT /prod/followers 
    const put_followers = this.createLambda("linkup-put-followers", "lambda", "linkup_put_followers.lambda_handler", labRole);

    /* globalFeed */

    // GET /prod/globalFeed 
    const get_globalFeed = this.createLambda("linkup-get-globalFeed", "lambda", "linkup_get_globalFeed.lambda_handler", labRole);

    /* index */

    // GET /prod/index
    const get_index = this.createLambda("linkup-get-index", "lambda", "linkup_get_index.lambda_handler", labRole);

    /* login */

    // GET /prod/login 
    const get_login = this.createLambda("linkup-get-login", "lambda", "linkup_get_login.lambda_handler", labRole);

    /* postDB */

    // POST /prod/postDB 
    const post_postDB = this.createLambda("linkup-post-postDB", "lambda", "linkup_post_postDB.lambda_handler", labRole);

    // GET /prod/postDB 
    const get_postDB = this.createLambda("linkup-get-postDB", "lambda", "linkup_get_postDB.lambda_handler", labRole);
    
    // PUT /prod/postDB
    const put_postDB = this.createLambda("linkup-put-postDB", "lambda", "linkup_put_postDB.lambda_handler", labRole);

    /* profile */

    // GET /prod/profile 
    const get_profile = this.createLambda("linkup-get-profile", "lambda", "linkup_get_profile.lambda_handler", labRole);

    /* register */

    // GET /prod/profile 
    const get_register = this.createLambda("linkup-get-register", "lambda", "linkup_get_register.lambda_handler", labRole);
  
    /* update */

    // GET /prod/update 
    const get_update = this.createLambda("linkup-get-update", "lambda", "linkup_get_update.lambda_handler", labRole);

    /* friendsFeed */

    // GET /prod/friendsFeed
    const get_friendsFeed = this.createLambda("linkup-get-friendsFeed", "lambda", "linkup_get_friendsFeed.lambda_handler", labRole);

    /* ---------- API Gateway ---------- */
    // api gateway for `LinkUp` Social Network
    const linkup_api_gateway = new apigateway.RestApi(this, 'linkup_api_gateway', {
      endpointTypes: [apigateway.EndpointType.REGIONAL],
      restApiName: 'linkup-api-gateway',
      description: 'LinkUp Social Network.', 
    });

    const db_resource = linkup_api_gateway.root.addResource("db");
    db_resource.addMethod("POST", new apigateway.LambdaIntegration(post_db, {
      proxy: false,
      integrationResponses: [
        {
          statusCode: "200",
          responseParameters: {
            "method.response.header.Content-Type": "'application/json'"
          }
        }
      ]
    }), {
      methodResponses: [
        {
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true
          }
        }
      ]
    });
    db_resource.addMethod("GET", new apigateway.LambdaIntegration(get_db));
    db_resource.addMethod("PUT", new apigateway.LambdaIntegration(put_db, {
      proxy: false,
      integrationResponses: [
        {
          statusCode: "200",
          responseParameters: {
            "method.response.header.Content-Type": "'application/json'"
          }
        }
      ]
    }), {
      methodResponses: [
        {
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true
          }
        }
      ]
    });
    db_resource.addMethod("DELETE", new apigateway.LambdaIntegration(delete_db, {
      proxy: false,
      integrationResponses: [
        {
          statusCode: "200",
          responseParameters: {
            "method.response.header.Content-Type": "'application/json'"
          }
        }
      ]
    }), {
      methodResponses: [
        {
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true
          }
        }
      ]
    });

    const followers_resource = linkup_api_gateway.root.addResource("followers");
    followers_resource.addMethod("POST", new apigateway.LambdaIntegration(post_followers,  {
      proxy: false,
      integrationResponses: [
        {
          statusCode: "200",
          responseParameters: {
            "method.response.header.Content-Type": "'application/json'"
          }
        }
      ]
    }), {
      methodResponses: [
        {
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true
          }
        }
      ]
    });
    followers_resource.addMethod("GET", new apigateway.LambdaIntegration(get_followers));
    followers_resource.addMethod("PUT", new apigateway.LambdaIntegration(put_followers,  {
      proxy: false,
      integrationResponses: [
        {
          statusCode: "200",
          responseParameters: {
            "method.response.header.Content-Type": "'application/json'"
          }
        }
      ]
    }), {
      methodResponses: [
        {
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true
          }
        }
      ]
    });

    const globalFeed_resource = linkup_api_gateway.root.addResource("globalFeed");
    globalFeed_resource.addMethod("GET", new apigateway.LambdaIntegration(get_globalFeed));

    const index_resource = linkup_api_gateway.root.addResource("index");
    index_resource.addMethod("GET", new apigateway.LambdaIntegration(get_index));

    const login_resouce = linkup_api_gateway.root.addResource("login");
    login_resouce.addMethod("GET", new apigateway.LambdaIntegration(get_login));

    const postDB_resource = linkup_api_gateway.root.addResource("postDB");
    postDB_resource.addMethod("POST", new apigateway.LambdaIntegration(post_postDB, {
      proxy: false,
      integrationResponses: [
        {
          statusCode: "200",
          responseParameters: {
            "method.response.header.Content-Type": "'application/json'"
          }
        }
      ]
    }), {
      methodResponses: [
        {
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true
          }
        }
      ]
    });
    postDB_resource.addMethod("GET", new apigateway.LambdaIntegration(get_postDB));
    postDB_resource.addMethod("PUT", new apigateway.LambdaIntegration(put_postDB, {
      proxy: false,
      integrationResponses: [
        {
          statusCode: "200",
          responseParameters: {
            "method.response.header.Content-Type": "'application/json'"
          }
        }
      ]
    }), {
      methodResponses: [
        {
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true
          }
        }
      ]
    });

    const profile_resource = linkup_api_gateway.root.addResource("profile");
    profile_resource.addMethod("GET", new apigateway.LambdaIntegration(get_profile));

    const register_resource = linkup_api_gateway.root.addResource("register");
    register_resource.addMethod("GET", new apigateway.LambdaIntegration(get_register));

    const update_resource = linkup_api_gateway.root.addResource("update");
    update_resource.addMethod("GET", new apigateway.LambdaIntegration(get_update));

    const friendsFeed_resource = linkup_api_gateway.root.addResource("friendsFeed");
    friendsFeed_resource.addMethod("GET", new apigateway.LambdaIntegration(get_friendsFeed));

    new cdk.CfnOutput(this, "API Endpoint", {
      value: linkup_api_gateway.url + "index",
    });
  }

  private createBucket(bucketName: string, role: cdk.aws_iam.IRole) {
    const bucket = new s3.Bucket(this, bucketName, {
      bucketName: bucketName,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL
    });
    bucket.grantReadWrite(role);

    return bucket;
  }

  private createLambda(functionName: string, location: string, handler: string, role: cdk.aws_iam.IRole) {
    return new lambda.Function(this, functionName, {
      runtime: lambda.Runtime.PYTHON_3_12,
      code: lambda.Code.fromAsset(location),
      handler: handler,
      role: role,
    });
  }

  private deployObjectToS3(objectPath: string, deploymentID: string, bucket: cdk.aws_s3.Bucket, role: cdk.aws_iam.IRole) {
    new BucketDeployment(this, deploymentID, {
      sources: [Source.asset(objectPath)],
      destinationBucket: bucket,
      role: role
    });
  }
}
