# DailyEncouragement

Use OpenAI, AWS Lambda, SNS, EventBridge and SAM to send an email at a set time each day

## Content

1. Introduction
2. Prerequisites
3. Build
4. Results

## Introduction

This project started off from feeling down and wanting to have something cheerful at the beginning of the day. I've been asking ChatGPT for advice, and thought I could use some aws services along with ChatGPT to send an email to me every day and give me words of encouragement. (It's not an amazing project, but wanted to try to link things together)

## Prerequisites

1. Need to have an AWS account and OpenAI account
   - Notes on creating OpenAI Account:
     1. Create an OpenAI account and set up paid version
     1. It is a pay for what you use pricing model
     1. You buy "tokens", which include both your prompt and the response
     1. It will initially deduct USD$5.00 and give you some free tokens to use for the first 3 months
     1. You can choose between different models and prices vary. For more: https://openai.com/pricing
     1. Check out some prompt examples: https://platform.openai.com/examples
2. Use Python 3.9 for Lambda Layer and for Lambda runtime

## Build

### Version 1: through AWS Console

1. Create Lambda function
2. Download OpenAI for lambda layer
   - Download at https://github.com/erenyasarkurt/OpenAI-AWS-Lambda-Layer?tab=readme-ov-file
   - cd to Downloads folder
   - Make new folder `mkdir python`
   - Install OpenAI locally `pip install openai -t .`
   - Go to outer folder `cd ..`
   - Create zip file for lambda layer `zip -r openai-lambda-package.zip python`
3. Create SNS Topic and subscribe using email
   1. On right hand side click on 'Topics'
   2. Select Standard SNS, and then click 'Create Topic'
   3. Create a subscription by clicking on 'Create Subsciption'
   4. Under 'Protocol', select 'Email', then add the target email under 'Endpoint'
   5. SNS will send you an email to activate the subscription, so remember to check your email
4. Connect Lambda to SNS
   1.  Add the following to your lambda function (don't forget to hit Deploy)
      ```
         import json
         import boto3
         import os
         
         def lambda_handler(event, context):
             # Set up SNS client
             sns = boto3.client('sns')
             
             message = event["message"]
             
             # Send the message to SNS
             sns_response = sns.publish(
                 TopicArn=os.environ['TOPIC_ARN'],
                 Message=message,
                 MessageStructure='string'
             )
             
             # Return a success response
             return {
                 'statusCode': 200,
                 'body': json.dumps(sns_response)
             }

      ```
   2. Create a `TOPIC_ARN` environment variable and copy the arn value of the sns topic
   3. Create Destination to point to that sns topic (to provide the correct permissions for the lambda function)
   4. Create Test, and configure an event (ex: "message": "Test sns and lambda connection")
   5. Should see a 200 from the Execution Results and should see an email with that message
5. Connect Lambda to OpenAI:
   2. Create Lambda Layer: scroll to the bottom where you see "Layers", click "Add a Layer", select "Custom layers"
      <img width="868" alt="Screenshot 2024-04-01 at 2 55 33 PM" src="https://github.com/athenasu/daily_encouragement/assets/71711844/e15257ff-ce85-4fcc-b9a2-f724e6b1e28f">
   3. Extend TTL for Lambda (default 3 secs, but it might take longer for the OpenAI library to set up)
   4. Add `OPENAI_API_KEY` environment variable
   5. Add openai to your code, do not send query yet, but test with sns connection to see if it connects:
      ```
      import json
      import boto3
      import openai
      import os
      
      SNS_TOPIC_ARN = os.environ['TOPIC_ARN']
      openai.api_key = os.environ['OPENAI_API_KEY']
      
      def lambda_handler(event, context):
          
          # Set up SNS client
          sns = boto3.client('sns')

          message = event["message"]
          
          # Send the message to SNS
          sns_response = sns.publish(
              TopicArn=os.environ['TOPIC_ARN'],
              Message=message,
              MessageStructure='string'
          )
          
          # Return a success response
          return {
              'statusCode': 200,
              'body': json.dumps(sns_response)
          }
      ```
   6. Once that passes, we can set up and hit the openai endpoint. Add a prompt from your event, create a ChatCompletion, get the message, and pass on to sns:
      ```
      import json
      import boto3
      import openai
      import os
      
      SNS_TOPIC_ARN = os.environ['TOPIC_ARN']
      openai.api_key = os.environ['OPENAI_API_KEY']
      
      def lambda_handler(event, context):
          
          # Set up SNS client
          sns = boto3.client('sns')
          
          prompt = event['prompt']
          
          response = openai.ChatCompletion.create(
              model='gpt-3.5-turbo',
              messages=[{"role": "user", "content": prompt}],
              max_tokens=50,
          )
          
          print(response)
          
          message = response['choices'][0]['message']['content'].strip()
          print(message)
          
          # Send the message to SNS
          sns_response = sns.publish(
              TopicArn=SNS_TOPIC_ARN,
              Message=json.dumps({'default': message}),
              MessageStructure = 'json'
           )
           
           # Return a success response
          return {
              'statusCode': 200,
              'body': json.dumps(sns_response)
          }
      ```
   8. Select Test and re-enter your prompt statement
6. Set up EventBridge cron job to trigger the Lambda function everyday (need to use the default event bus to use the scheduler functionality)
   1. Go to EventBridge and select 'Rules'
   2. Click on 'Create rule', fill in the information for the rule, select 'default' for 'Event bus', and click on 'Schedule'. Click 'Next'
   3. Then select 'Recurring schedule' and fill in the cron expression (https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html?icmpid=docs_console_unmapped#cron-based)

### Version 2: Through SAM & CLI (WIP)

1. Fork repo
2. Make sure you have a Lambda layer that downloads OpenAI
3. Make sure to fill out:
   - template.yaml line 16: your region (ex: us-west-2)
   - template.yaml line 17: your arn for the OpenAI Lambda layer
   - hello_world/app.py line 7: your OpenAI key
   - hello_world/app.py line 28: add your SNS topic ARN
4. Run:
   1. In terminal, run `sam build`, `sam validate`, and then `sam deploy --guided`
   2. Go to SNS in console and subscribe through email
   3. Go to EventBridge console and set up cron job

### TODOs

1. ~~Use SAM to automate CloudFormation & deployment~~
2. Automate SNS subsciption for emails
3. Configure cron job for EventBridge
4. Create Frontend to be able to select what type of daily emails to get and set up time
