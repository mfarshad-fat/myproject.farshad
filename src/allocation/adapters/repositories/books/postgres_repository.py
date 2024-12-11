
from sqlalchemy.orm import Session
from src.allocation.adapters.models import Books
from src.allocation.domain.entities import BooksBase
from src.allocation.adapters.connector.redis import redis_client

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_book_by_isbn(self, isbn: str):
        return self.db.query(Books).filter(Books.isbn == isbn).first()

    def get_by_id(self, book_id:int) :
        return self.db.query(Books).filter(Books.book_id==book_id).first()
    
    def create_book(self, book_data: BooksBase):
        new_book = Books(**book_data.dict())
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def update_book(self, book_id: int, book_data: BooksBase):
        db_book = self.db.query(Books).filter(Books.book_id == book_id).first()
        if not db_book:
            return None
        for key, value in book_data.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id: int):
        db_book = self.db.query(Books).filter(Books.book_id == book_id).first()
        if not db_book:
            return None
        self.db.delete(db_book)
        self.db.commit()
        return db_book