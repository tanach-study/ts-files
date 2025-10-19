import os
import boto3
from django.conf import settings

# Only initialize boto3 client if not in CI environment
if not os.getenv('CI'):
    client = boto3.client(
        "elastictranscoder",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
else:
    client = None
