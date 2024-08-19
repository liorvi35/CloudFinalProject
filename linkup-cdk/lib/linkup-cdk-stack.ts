import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class LinkupCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    const labRole = iam.Role.fromRoleArn(this, 'Role', "arn:aws:iam::991888206011:role/LabRole", { mutable: false });
  
    const storage = new s3.Bucket(this, 'MyBucket', {
      bucketName: 'my-bucket-name',
      versioned: true, // Optional: Enable versioning for the bucket
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Optional: Automatically delete the bucket when the stack is deleted
      autoDeleteObjects: true // Optional: Automatically delete all objects in the bucket when the stack is deleted
    });


  }
}
