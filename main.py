import boto3
import os
import json
import base64
from io import BytesIO

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
FILES_DIR = os.path.join(ROOT_DIR, "files")

def list_buckets():
    s3 = boto3.resource("s3")
    return [bucket.name for bucket in s3.buckets.all()]


def download_file_from_s3(filename: str, path_to_download: str) -> bool:
    s3 = boto3.client("s3")
    try:
        s3.download_file(
            Bucket="ilterisbucket",
            Key=filename,
            Filename=os.path.join(path_to_download, f"downloaded_{filename}")
        )
        return True
    except Exception as e:
        print(e)
        return False


def upload_file_to_s3(filepath: str, upload_name: str):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(
            Bucket="ilterisbucket",
            Filename=filepath,
            Key=upload_name
        )
        return True
    except Exception as e:
        print(e)
        return False


def get_bucket_access_policy(bucket_name: str):
    s3 = boto3.client("s3")
    return s3.get_bucket_acl(Bucket=bucket_name)


def upload_file_as_base64(filepath: str, path_to_upload: str):
    s3 = boto3.resource("s3")
    try:
        with open(filepath, "rb") as image_file:
            base64encoded = base64.b64encode(image_file.read())
        buffer = BytesIO(base64.b64decode(base64encoded))
        s3.Bucket("ilterisbucket").put_object(
            Body=buffer,
            Key=path_to_upload
        )
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    bucket_list = list_buckets()
    for bucket in bucket_list:
        print(f"{bucket} : {json.dumps(get_bucket_access_policy(bucket), indent=2)}")

    status = upload_file_as_base64("/home/ilteris/Pictures/test.jpeg", "test.jpeg")
    print(status)

