from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

books =  []

class Book(BaseModel):
    title: str
    author: str
    price: int
   

@app.post("/books")
def create_book(book: Book):
    
    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "author": book.author,
        "price": book.price
    }
    
    books.append(new_book)
    
    return new_book


@app.get("/books")
def get_books():
    return books

@app.get("/books/{books_id}")
def get_book(books_id: int):
    
    for book in books:
        if book["id"] == book.id:
            return book
    
    return {
        "message": "Book not found"
    }

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    
    for book in books:
        if book["id"] == book_id:
            book["title"] = book.title
            book["author"] = book.author
            book["price"] = book.price
            
            return book
        
    return {
        "message": "Book not found"
    }

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {
                "message": "Book deleted successfully"
            }
    raise  HTTPException(
        status_code =  404,
        detail = "Book not found"
    )
   
