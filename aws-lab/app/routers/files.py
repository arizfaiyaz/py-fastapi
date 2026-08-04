import logging
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
    ProfileNotFound,
)
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.core.config import Settings, get_settings
from app.schemas.files import FileUploadResponse
from app.services.s3_service import S3Service, get_s3_service


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


ALLOWED_FILE_TYPES: dict[str, set[str]] = {
    "image/jpeg": {".jpg", ".jpeg"},
    "image/png": {".png"},
    "image/webp": {".webp"},
}


@router.post(
    "/upload",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_file(
    file: Annotated[
        UploadFile,
        File(description="Upload a JPG, JPEG, PNG, or WEBP image"),
    ],
    settings: Annotated[Settings, Depends(get_settings)],
    s3_service: Annotated[S3Service, Depends(get_s3_service)],
) -> FileUploadResponse:
    """Validate an uploaded image and store it in Amazon S3."""

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file must have a filename.",
        )

    safe_filename = Path(file.filename).name
    file_extension = Path(safe_filename).suffix.lower()
    content_type = file.content_type or "application/octet-stream"

    allowed_extensions = ALLOWED_FILE_TYPES.get(content_type)

    if allowed_extensions is None or file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported file type. "
                "Only JPG, JPEG, PNG, and WEBP images are allowed."
            ),
        )

    # Move to the end of the file to determine its size.
    file.file.seek(0, 2)
    file_size = file.file.tell()

    # Move back to the beginning before uploading.
    file.file.seek(0)

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty.",
        )

    maximum_size_bytes = settings.max_upload_size_mb * 1024 * 1024

    if file_size > maximum_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                f"The file is too large. "
                f"Maximum size is {settings.max_upload_size_mb} MB."
            ),
        )

    unique_filename = f"{uuid4().hex}{file_extension}"
    object_key = f"uploads/images/{unique_filename}"

    try:
        s3_service.upload_file(
            file_object=file.file,
            object_key=object_key,
            content_type=content_type,
        )

    except ProfileNotFound as error:
        logger.exception("The configured AWS profile was not found.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The configured AWS profile was not found.",
        ) from error

    except NoCredentialsError as error:
        logger.exception("AWS credentials were not found.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AWS credentials were not found.",
        ) from error

    except ClientError as error:
        logger.exception("Amazon S3 rejected the upload request.")

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Amazon S3 rejected the upload request.",
        ) from error

    except BotoCoreError as error:
        logger.exception("The AWS SDK could not complete the upload.")

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AWS SDK could not complete the upload.",
        ) from error

    return FileUploadResponse(
        message="File uploaded successfully",
        original_filename=safe_filename,
        object_key=object_key,
        content_type=content_type,
        size_bytes=file_size,
    )