 
# entrypoint/routes/books.py

from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.orm import Session
import src.allocation.service_layer.helpers.jwt_auth as jwt
from src.allocation.adapters.connector.database import get_db
from src.allocation.domain.entities import BooksBase, BooksOut, BooksUpdate
import src.allocation.adapters.models as models
from src.allocation.domain.entities.userjwt_schemas import TokenData

router = APIRouter()

@router.get("/", response_model=list[BooksOut])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    books = db.query(models.Books).offset(skip).limit(limit).all()
    return books

@router.post("/", response_model=BooksBase)
def create_book(book: BooksBase, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_book = db.query(models.Books).filter(models.Books.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    new_book = models.Books(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{book_id}", response_model=BooksOut)
def update_book(book_id: int, book: BooksUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_book = db.query(models.Books).filter(models.Books.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_book = db.query(models.Books).filter(models.Books.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted successfully"}
