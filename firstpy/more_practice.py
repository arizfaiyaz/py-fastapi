from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items")
def create_item(item: Item):
    
    new_item = {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax
    }

    return new_item

@app.get