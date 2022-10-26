from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from services.book import insert_book,read_books
from schemas.book import BookIn
from utils.db import get_db

book = APIRouter()

@book.post("/")
def add_book(book:BookIn,db:Session=Depends(get_db)):
    insert_book(db=db,book=book)
    return {
        "code":"0000",
        "msg":"OK"
    }

@book.get("/")
def get_books(db:Session=Depends(get_db)):
    data = read_books(db=db)
    return {
        "code": "0000",
        "msg": "OK",
        "data": data
    }