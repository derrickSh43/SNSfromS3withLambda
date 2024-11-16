import json
import boto3
import os

sns_client = boto3.client('sns')

# add Key:"SNS_TOPIC_ARN" and Value:"your SNS ARN here"
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    # Extract S3 event details
    records = event.get('Records', [])
    if not records:
        return {"statusCode": 400, "body": "No records found"}

    for record in records:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        event_time = record['eventTime']
        event_name = record['eventName']
        region = record['awsRegion']
        object_size = record['s3']['object'].get('size', 'Unknown')

        # Format the email content with proper line breaks
        message = (
            f"New S3 Upload Notification\n\n"
            f"Bucket: {bucket_name}\n"
            f"File: {object_key}\n"
            f"Size: {object_size} bytes\n"
            f"Event Time: {event_time}\n"
            f"Region: {region}\n"
            f"Event Type: {event_name}\n\n"
            f"View the file: https://s3.console.aws.amazon.com/s3/object/{bucket_name}?region={region}&prefix={object_key}"
        )

        # Send the formatted message to SNS
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="S3 Upload Notification"
        )

    return {"statusCode": 200, "body": "Message sent to SNS"}
