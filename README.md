# CloudFinalProject
Final project in "Big Data &amp; Cloud Computing" course at Ariel-University.

## Table of Contents
- [Introduction](#Introduction)
- [Authors](#Authors)
- [Installation](#Installation)
- [Cloud](#Cloud)
- [Demo](#Demo)
- [Features](#Features)
- [License](#License)

## Introduction

We've implemented and deployed a social network web application using AWS cloud infrastracture.

## Authors
- [Lior Vinman](https://github.com/liorvi35)
- [Yoad Tamar](https://github.com/YoadTamar)

## Installation
### Install AWS CLI
```bash
# Download the AWS CLI 
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Unzip the package
unzip awscliv2.zip

# Install the AWS CLI
sudo ./aws/install

# Clean up the installation files 
rm -rf awscliv2.zip aws
```

### Set your Credentials
Run `aws configure` then update your account keys and configurations at `~/.aws/credentials` and `~/.aws/config`.

for verification, run `aws s3 ls`, and make sure that you see some s3 bucket from you account. 

### Install AWS CDK 
```bash
# Install Typescript
npm -g install typescript

# Install CDK
npm install -g aws-cdk

# Verify that CDK Is installed
cdk --version
```

### Bootstrap your account for CDK
> Note that: If you already bootstrap your account, no need to execute that action
```bash
# Go to CDK
cd linkup-cdk

# Install NPM models
npm install

# Run bootsrap
cdk bootstrap --template bootstrap-template.yaml
```

### Deploy the Base Stack
Deploy the infrastracture to the cloud using:
```bash
cdk deploy
```

## Cloud
Here are the cloud infrastracture components we've used:

- (AWS) API Gateway (REST API)
- (AWS) Lambda Functions and Layers
- (AWS) S3
- (AWS) DynamoDB
- (AWS) SQS
- (AWS) Rekognition
- (Azure) OpenAI

## Demo
Here is presented a full demo video for our social media network application:

https://github.com/user-attachments/assets/f2edb98d-44ae-4c26-998c-f1f39faf6762

## Features

### Flow Diagrams and Main Features
Here are presented some flow diagrams for main application features (all could be seen in the video above):

### Image Processing to Post Pictures
<center><img src="https://github.com/liorvi35/CloudFinalProject/blob/main/flow_diagrams/image_processing.png" alt="description of the image"></center>

### Send a TL;DR Email
<center><img src="https://github.com/liorvi35/CloudFinalProject/blob/main/flow_diagrams/email_summery.png" alt="description of the image"></center>

### Comment Behavior Classification
<center><img src="https://github.com/liorvi35/CloudFinalProject/blob/main/flow_diagrams/comment_classification.png" alt="description of the image"></center>

### Register a New User / Delete an Existing User / Upload a Profile Picture
<center><img src="https://github.com/liorvi35/CloudFinalProject/blob/main/flow_diagrams/register_delete_profile.png" alt="description of the image"></center>

### Login to Existing User
<center><img src="https://github.com/liorvi35/CloudFinalProject/blob/main/flow_diagrams/login.png" alt="description of the image"></center>

## License
This project is licensed under the GNU GPLv3 License. See the LICENSE file for details.
