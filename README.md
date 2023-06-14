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
2. Use Python 3.9

## Build

### Version 1: through AWS Console

1. Install OpenAI
   - Install OpenAI locally `pip install openai`
   - Install OpenAI for Lambda `pip install openai --target <path_for_openai_library>`
     _put all files in single folder and compress to zip file_
2. Create SNS Topic and subscribe using email
   1. On right hand side click on 'Topics'
   2. Click 'Create Topic'
   3. Click on the topic you created, and click 'Create Subsciption'
   4. Under 'Protocol', select 'Email', then add the target email under 'Endpoint'
   5. SNS will send you an email to activate the subscription, so remember to check your email
3. Create Lambda function (from aws console)
   1. Check to see Lambda can publish an SNS message
   2. Create Lambda Layer: Add OpenAI library to Lambda layer, then add layer to Lambda
   3. Extend TTL for Lambda (default 3 secs, but it might take longer for the OpenAI library to set up)
4. Set up EventBridge cron job to trigger the Lambda function everyday (need to use the default event bus to use the scheduler functionality)
   1. Go to EventBridge and select 'Rules'
   2. Click on 'Create rule', fill in the information for the rule, select 'default' for 'Event bus', and click on 'Schedule'. Click 'Next'
   3. Then select 'Recurring schedule' and fill in the cron expression (https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html?icmpid=docs_console_unmapped#cron-based)
5. Can create environment variable for the Lambda to store API key

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
