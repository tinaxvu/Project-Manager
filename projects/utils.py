import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def get_signed_url(file_upload):
    s3_client = boto3.client('s3',
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             region_name=settings.AWS_S3_REGION_NAME)

    try:
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                       'Key': file_upload.file.name},
                                               ExpiresIn=3600)  # URL valid for 1 hour
        return url
    except ClientError as e:
        print(e)
        return None
