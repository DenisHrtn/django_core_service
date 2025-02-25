import boto3
from botocore.exceptions import ClientError

AWS_REGION = "us-east-1"
AWS_ENDPOINT_URL = "http://localstack:4566"


def send_email_via_ses(subject, body, to_address):
    """
    Синхронная функция для отправки email через AWS SES.
    """
    client = boto3.client(
        "ses",
        region_name=AWS_REGION,
        endpoint_url=AWS_ENDPOINT_URL,
        aws_secret_access_key="test-secret-key",
        aws_access_key_id="test-access-key",
    )

    client.verify_email_identity(EmailAddress="test@gmail.com")

    try:
        response = client.send_email(
            Source="test@gmail.com",
            Destination={
                "ToAddresses": [to_address],
            },
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )
        print("Email sent successfully:", response)
    except ClientError as e:
        print("Failed to send email:", e)
