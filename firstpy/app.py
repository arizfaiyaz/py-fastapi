from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.get("/")
def home():
    return {"message": "Hello world in python!!"}

@app.get("/about")
def about():
    return {"name": "Jone doe"}

@app.get("/contact")
def contact():
    return {
        "email": "test@test.com"
    }
@app.post("/users") # Create a new user
def create_user(user: User):
    return {
        "username": user.name,
        "age": user.age,          
        # this is because user is a object of User class and we can access the attributes of the class using dot notation
        
        "details": [
            {
               "type": "int_parsing",
               "msg": "age must be an integer" 
            }
        ]
    }

@app.get("/users/{user_id}") # Get a specific user by ID
def get_user(user_id: int):
    return {
        "id": user_id
    }
    
#
@app.get("/users/{user_id}/posts/{post_id}") # Get a specific post of a specific user by user ID and post ID
def get_user_post(user_id: int, post_id:int):
    return {
        "id": user_id,
        "post_id": post_id
    }

# Query parameters
@app.get("/products")
def get_products(
    page:int=1,
    limit:int=10
):
    return {
        "page": page,
        "limit": limit
    }
    
# optional query parameters
@app.get("/search")
def search(q: str | None = None):
    return {
        "query": q
    }

#mixing both 
@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    details: bool=False
): 
    return {
        "id": user_id,
        "details": details
    }

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {
        "message": f"user {user_id} deleted"
    }
