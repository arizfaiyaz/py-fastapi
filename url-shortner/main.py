from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import column, create_engine, Column, Integer, String
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
    id = column(Integer, primary_key=True, index=True)
    original_url = column(String, unique=True, nullable=False)
    

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])