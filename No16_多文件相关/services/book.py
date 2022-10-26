from sqlalchemy.orm import Session
from datetime import datetime
from typing import Union

from models.book import Book
from schemas.book import BookIn

def insert_book(db:Session,book:BookIn):
    book = Book(title=book.title,author=book.author,publisher=book.publisher,code=book.code)
    db.add(book)
    db.commit()
    return True

def read_books(db:Session) -> list:
    books = db.query(Book).all()
    if books:
        result = []
        for book in books:
            result.append({
                "id":book.id,
                "title":book.title,
                "author":book.author,
                "publisher":book.publisher,
                "code":book.code
            })
        return result
