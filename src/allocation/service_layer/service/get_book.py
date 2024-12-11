from src.allocation.adapters.repositories.books.redis_repository import RedisRepository
from typing import List, Optional
from src.allocation.domain.entities import BooksOut

class GetBooksService:
    def __init__(self, redis_repository: RedisRepository):
        self.redis_repository = redis_repository

    def execute(self, skip: int, limit: int, title: Optional[str] = None, sort_by: Optional[str] = None, order: str = "asc") -> List[BooksOut]:
        books = self.redis_repository.get_all_books()

        # فیلتر کردن بر اساس عنوان
        if title:
            books = [book for book in books if title.lower() in book.get('title', '').lower()]

        # مرتب‌سازی
        if sort_by:
            reverse_order = order == "desc"
            books = sorted(books, key=lambda x: float(x.get(sort_by, 0)), reverse=reverse_order)

        # محدودیت و بازگشت
        return books[skip:skip + limit]
