from pydantic import BaseModel, Field, EmailStr

from firstpy import app

class User(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=18, le=100)
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    
@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user",
)
def create_user(user: User):
    return user


