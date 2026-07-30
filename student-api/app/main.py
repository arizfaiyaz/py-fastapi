from fastapi import FastAPI

from app.database import Base, engine

from app.routers import students

from app.models.student import Student

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(
    students.router
)
