import json
import boto3
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def hello(event, context):
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def send_email(event, context):
    logger.info("Received event: %s", event)
    print("Received event:", event)  # Additional print statement for debugging
    try:
        # Parse request body
        body = json.loads(event['body'])
        receiver_email = body['receiver_email']
        subject = body['subject']
        body_text = body['body_text']

        logger.info("Parsed email data: receiver_email=%s, subject=%s", receiver_email, subject)
        print("Parsed email data: receiver_email={}, subject={}".format(receiver_email, subject))  # Additional print statement for debugging

        # Create a new SES resource and specify a region.
        ses_client = boto3.client(
            'ses',
            region_name='us-east-1',
            aws_access_key_id='AKIA5FTZAXSTTKPLPWUT',
            aws_secret_access_key='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'
        )

        # The email sender address must be verified in SES.
        sender_email = 'subhashribehera1995@gmail.com'
        logger.info("Using sender email: %s", sender_email)
        print("Using sender email:", sender_email)  # Additional print statement for debugging

        # Send the email.
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [receiver_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8',
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8',
                    },
                },
            },
        )

        logger.info("Email sent! Response: %s", response)
        print("Email sent! Response:", response)  # Additional print statement for debugging

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent successfully!'}),
        }

    except ClientError as e:
        logger.error("ClientError: %s", e)
        print("ClientError:", e)  # Additional print statement for debugging
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)}),
        }
    except Exception as e:
        logger.error("Exception: %s", e)
        print("Exception:", e)  # Additional print statement for debugging
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
        }
