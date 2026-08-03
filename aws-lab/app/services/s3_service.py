from functools import lru_cache
from typing import BinaryIO

import boto3

from app.core.config import Settings, get_settings


class S3Service:
    """Handles communication between the application and Amazon S3."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _create_client(self):
        """
        Create an S3 client.

        Locally, Boto3 uses the named AWS CLI profile.
        Later on EC2, we can remove the profile and use an IAM role.
        """

        session_options: dict[str, str] = {
            "region_name": self.settings.aws_region,
        }

        if self.settings.aws_profile:
            session_options["profile_name"] = self.settings.aws_profile

        session = boto3.Session(**session_options)

        return session.client("s3")

    def upload_file(
        self,
        file_object: BinaryIO,
        object_key: str,
        content_type: str,
    ) -> None:
        """Upload a file-like object to the configured S3 bucket."""

        s3_client = self._create_client()

        s3_client.upload_fileobj(
            Fileobj=file_object,
            Bucket=self.settings.s3_bucket_name,
            Key=object_key,
            ExtraArgs={
                "ContentType": content_type,
            },
        )


@lru_cache
def get_s3_service() -> S3Service:
    """Create one reusable S3 service object."""

    return S3Service(settings=get_settings())