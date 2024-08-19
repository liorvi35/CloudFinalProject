import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';

export class LinkupCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    const labRole = iam.Role.fromRoleArn(this, 'Role', "arn:aws:iam::114985187174:role/LabRole", { mutable: false });
  
    // create stack here using labRole
  }
}
