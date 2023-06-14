import json
import boto3
import openai
import os

# Set up OpenAI API client
openai.api_key = {OpenAI_Key}

def lambda_handler(event, context):
    # Set up SNS client
    sns = boto3.client('sns')
    
    # Set up prompt for OpenAI
    prompt = "Provide inspiration for someone to start their day:"
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
    )
    
    print(response)
    
    message = response.choices[0].text
    
    # Send the message to SNS
    sns_response = sns.publish(
        TopicArn={arn_of_sns_topic_created},
        Message=json.dumps({'default': message}),
        MessageStructure = 'json'
    )
    
    # Return a success response
    return {
        'statusCode': 200,
        'body': json.dumps(sns_response)
    }
