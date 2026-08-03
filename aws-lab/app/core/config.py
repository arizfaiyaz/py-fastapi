from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "FastAPI S3 File API"

    aws_profile: str | None = None
    aws_region: str = "ap-south-1"
    s3_bucket_name: str

    max_upload_size_mb: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Create the settings object once and reuse it."""

    return Settings()