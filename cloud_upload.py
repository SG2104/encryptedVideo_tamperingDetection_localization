import boto3
import os

BUCKET_NAME = "your-s3-bucket-name"

def upload_to_s3(file_path, object_name=None):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id="your-access-key-id",
        aws_secret_access_key="your-secret-access-key",
        region_name="your-region"
    )
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client.upload_file(file_path, BUCKET_NAME, object_name)
