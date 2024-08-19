import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { AutoScalingGroup } from 'aws-cdk-lib/aws-autoscaling';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as elasticache from 'aws-cdk-lib/aws-elasticache';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as s3Deployment from 'aws-cdk-lib/aws-s3-deployment';

export class LinkupCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const labRole = iam.Role.fromRoleArn(this, 'Role', "arn:aws:iam::991888206011:role/LabRole", { mutable: false });

    const deploymentBucket = this.deployTheApplicationArtifactToS3Bucket(labRole, "yoad-tamar-123456");
  }

  private deployTheApplicationArtifactToS3Bucket(labRole: cdk.aws_iam.IRole, bucketName: string) {
    const bucket = new s3.Bucket(this, bucketName, {
      removalPolicy: cdk.RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
    });

    // Output the bucket name
    new cdk.CfnOutput(this, bucketName, {
      value: bucket.bucketName,
    });
    return bucket;
  }
}
