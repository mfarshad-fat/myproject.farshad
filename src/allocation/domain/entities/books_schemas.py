from pydantic import BaseModel
from typing import Optional

class BooksBase(BaseModel):
    title:Optional[str] = None 
    author:Optional[str] = None
    isbn:Optional[str] = None
    published_year:Optional[int] = None
    genre:Optional[str] = None
    total_copies:Optional[int] = None
    price:Optional[str] = None
    access_id :Optional[int] = None
    
    def validate_for_create(self):
        missing_fields = [
            field
            for field in ["title", "author", "isbn", "published_year","genre","total_copies","price","access_id"]
            if getattr(self, field) is None
        ]
        if missing_fields:
            raise ValueError(f"Missing required fields for creation: {', '.join(missing_fields)}") 
    

class BooksOut(BooksBase):  # برای GET
    book_id: int

