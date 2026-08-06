from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import sessionmaker, declarative_base, session
from sqlalchemy import Column, create_engine, Integer, String
from fastapi.responses import RedirectResponse
import string, random

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
    
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)

Base.metadata.create_all(bind=engine)

class URLRequest(BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    original_url: str
    short_code: str
    short_url: str
    
    class COnfig:
        orm_mode = True

def generate_short_code(length = 6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


app = FastAPI(title="URL Shortener", description="A simple URL shortener API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
