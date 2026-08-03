from pathlib import Path

import boto3
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
    ProfileNotFound,
)


PROFILE_NAME = "ariz-s3"
REGION_NAME = "ap-south-1"

# Replace this with your exact S3 bucket name.
BUCKET_NAME = "ariz-learning-s3-2026-01"

# The file that already exists on your computer.
LOCAL_UPLOAD_FILE = Path("python-upload.txt")

# The new local file that will be created after downloading from S3.
LOCAL_DOWNLOAD_FILE = Path("python-downloaded.txt")

# The object's complete key inside the S3 bucket.
OBJECT_KEY = "uploads/python-upload.txt"


def create_s3_client():
    """Create an S3 client using the named AWS CLI profile."""

    session = boto3.Session(
        profile_name=PROFILE_NAME,
        region_name=REGION_NAME,
    )

    return session.client("s3")


def main() -> None:
    if BUCKET_NAME == "YOUR_BUCKET_NAME":
        raise ValueError(
            "Replace YOUR_BUCKET_NAME in s3_test.py with your real bucket name."
        )

    if not LOCAL_UPLOAD_FILE.exists():
        raise FileNotFoundError(
            f"Required file does not exist: {LOCAL_UPLOAD_FILE.resolve()}"
        )

    try:
        s3 = create_s3_client()

        print("1. Uploading file...")
        s3.upload_file(
            Filename=str(LOCAL_UPLOAD_FILE),
            Bucket=BUCKET_NAME,
            Key=OBJECT_KEY,
        )
        print(f"Uploaded to s3://{BUCKET_NAME}/{OBJECT_KEY}")

        print("\n2. Downloading file...")
        s3.download_file(
            Bucket=BUCKET_NAME,
            Key=OBJECT_KEY,
            Filename=str(LOCAL_DOWNLOAD_FILE),
        )
        print(f"Downloaded to {LOCAL_DOWNLOAD_FILE.resolve()}")

        downloaded_content = LOCAL_DOWNLOAD_FILE.read_text(encoding="utf-8")
        print("\nDownloaded file content:")
        print(downloaded_content)

        print("\n3. Deleting object from S3...")
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=OBJECT_KEY,
        )
        print(f"Deleted s3://{BUCKET_NAME}/{OBJECT_KEY}")

        print("\nS3 Boto3 test completed successfully.")

    except ProfileNotFound:
        print(
            f'AWS profile "{PROFILE_NAME}" was not found. '
            "Run aws configure --profile ariz-s3-learning."
        )

    except NoCredentialsError:
        print("AWS credentials were not found.")

    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code", "Unknown")
        error_message = error.response.get("Error", {}).get(
            "Message",
            "No error message returned.",
        )

        print(f"AWS ClientError [{error_code}]: {error_message}")

    except BotoCoreError as error:
        print(f"AWS SDK error: {error}")


if __name__ == "__main__":
    main()