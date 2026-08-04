from fastapi import FastAPI

from app.core.config import get_settings
from app.routers.files import router as files_router


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="A small FastAPI project for storing private files in Amazon S3.",
    version="0.1.0",
)


@app.get(
    "/health",
    tags=["Health"],
)
def health_check() -> dict[str, str]:
    """Check whether the API is running."""

    return {
        "status": "ok",
    }


app.include_router(files_router)