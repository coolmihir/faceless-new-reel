import boto3
import os

def upload_to_r2(file_path, object_name=None):
    access_key = os.getenv("R2_ACCESS_KEY")
    secret_key = os.getenv("R2_SECRET_KEY")
    account_id = os.getenv("R2_ACCOUNT_ID")
    bucket = os.getenv("R2_BUCKET")
    region = os.getenv("R2_REGION", "auto")

    if object_name is None:
        object_name = os.path.basename(file_path)

    endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"

    s3 = boto3.client(
        's3',
        region_name=region,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    s3.upload_file(file_path, bucket, object_name)

    return f"{endpoint_url}/{bucket}/{object_name}"
