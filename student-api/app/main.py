from fastapi import FastAPI

from app.routers import students

app = FastAPI()

app.include_router(
    students.router
)
