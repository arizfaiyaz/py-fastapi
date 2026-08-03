from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    """Response returned after a successful S3 upload."""

    message: str
    original_filename: str
    object_key: str
    content_type: str
    size_bytes: int