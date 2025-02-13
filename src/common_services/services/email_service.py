import aioboto3
from asgiref.sync import async_to_sync
from botocore.exceptions import ClientError

AWS_REGION = "us-east-1"
AWS_ENDPOINT_URL = "http://localstack:4566"


@async_to_sync
async def send_email_via_ses(subject, body, to_address):
    async with aioboto3.client(
        "ses",
        region_name=AWS_REGION,
        endpoint_url=AWS_ENDPOINT_URL,
        aws_secret_access_key="test-secret-key",
        aws_access_key_id="test-access-key",
    ) as client:
        try:
            response = await client.send_email(
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
