import boto3
from django.conf import settings

client = boto3.client(
    'elastictranscoder',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
