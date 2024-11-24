 
# entrypoint/routes/books.py
# جست و جو در عنوان
# فیلتر ها :
# قیمت
# عنوان کتاب
# ژانر
# id باید بده
# سورت کردن بر اساس قیمت (گران ترین و ارزان ترین)

from fastapi import APIRouter, Depends, HTTPException , Query , Path, Body , Request
from sqlalchemy.orm import Session
import src.allocation.service_layer.helpers.jwt_auth as jwt
from src.allocation.adapters.connector.postgres import get_db
from src.allocation.adapters.connector.redis import redis_client
from src.allocation.domain.entities import BooksBase, BooksOut
import src.allocation.adapters.models as models
from src.allocation.domain.entities import TokenData
from src.allocation.entrypoint.dependencies.rate_limiter import RateLimiter
import redis

router = APIRouter()
rate_limiter = RateLimiter()

@router.get("/", response_model=list[BooksOut])
async def read_books(
    request: Request ,
    skip: int = 0 , 
    limit: int = 10,
    title: str = None,               
    sort_by: str = None,              
    order: str = "asc",               
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(jwt.get_current_user)
) :
    client_ip = request.client.host
    if rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")   
    
    books = []

    # بازیابی کلیدهای کتاب
    book_keys = redis_client.lrange("books", 0, -1)

    for book_key in book_keys:
        book_info = redis_client.hgetall(book_key)

        # تبدیل داده‌های Redis به دیکشنری پایتون
        book_data = {k: v for k, v in book_info.items()}

        # اعمال فیلترها
        if title and title.lower() not in book_data.get('title', '').lower():
            continue


        books.append(BooksOut(**book_data))

    # اعمال مرتب‌سازی بر اساس فیلتر انتخابی
    if sort_by:
        if sort_by in ["price", "book_id"]:  # بررسی نوع فیلتر معتبر
            reverse_order = order == "desc"
            try:
                books = sorted(books, key=lambda x: float(getattr(x, sort_by)), reverse=reverse_order)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid value for sorting by {sort_by}")
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by parameter. Choose 'price' or 'book_id'.")

    # اعمال محدودیت skip و limit
    return books[skip:skip + limit]

    # db_books = db.query(models.Books).all()
    # if not db_books:
    #     raise HTTPException(status_code=404, detail="هیچ کتابی یافت نشد.")


    # books = db.query(models.Books).offset(skip).limit(limit).all()
    # return books

@router.post("/", response_model=BooksOut)
def create_book(request: Request , book: BooksBase, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    client_ip = request.client.host
    if rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")   
        
    db_book = db.query(models.Books).filter(models.Books.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    # ایجاد کتاب جدید در پایگاه داده
    new_book = models.Books(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    # آماده‌سازی داده‌ها برای ذخیره در Redis
    book_data = book.dict()  
    book_data["book_id"] = new_book.book_id  # افزودن book_id از دیتابیس
    
    # ذخیره داده‌های کتاب در Redis
    book_key = f"book:{new_book.book_id}"  # استفاده از book_id به عنوان کلید
    redis_client.hset(book_key, mapping=book_data)
    redis_client.rpush("books", book_key)

    return new_book


@router.put("/{book_id}", response_model=BooksOut)
def update_book(
    request : Request , 
    book_id: int, 
    book: BooksBase, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(jwt.get_current_user)
):
    client_ip = request.client.host
    if rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")   

    # جستجوی کتاب در پایگاه‌داده
    db_book = db.query(models.Books).filter(models.Books.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # به‌روزرسانی مقادیر کتاب در پایگاه‌داده
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)

    # به‌روزرسانی کتاب در Redis
    book_key = f"book:{book_id}"
    redis_client.hset(book_key, mapping={**book.dict(exclude_unset=True)})

    return db_book


@router.delete("/{book_id}")
def delete_book(request : Request , book_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    client_ip = request.client.host
    if rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")  
    
    db_book = db.query(models.Books).filter(models.Books.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()

    book_key = f"book:{book_id}"
    redis_client.delete(book_key)
    redis_client.lrem("books", 0, book_key)  # حذف کلید کتاب از لیست "books"

    return {"detail": "Book deleted successfully"}
