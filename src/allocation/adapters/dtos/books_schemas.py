from pydantic import BaseModel
from typing import Optional

class BooksBase(BaseModel):
    title:str
    author:str
    isbn:str
    published_year:int
    genre:str
    total_copies:str  
    access_id : int


class BooksOut(BooksBase):  # برای GET
    book_id: int

class BooksUpdate(BaseModel):  # مدل جدید برای PUT
    title:Optional[str] = None 
    author:Optional[str] = None
    isbn:Optional[str] = None
    published_year:Optional[int] = None
    genre:Optional[str] = None
    total_copies:Optional[str] = None  