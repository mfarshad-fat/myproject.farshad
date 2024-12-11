from src.allocation.adapters.repositories.books.redis_repository import RedisRepository
from src.allocation.adapters.repositories.books.postgres_repository import BookRepository
from src.allocation.domain.entities import BooksBase
from src.allocation.service_layer.helpers.exception_service import ExceptionService
class UpdateBookService:
    def __init__(self, book_repository: BookRepository, redis_repository: RedisRepository):
        self.book_repository = book_repository
        self.redis_repository = redis_repository

    def execute(self, book_id: int, book_data: BooksBase):
        # بررسی وجود کتاب در پایگاه داده
        book = self.book_repository.get_by_id(book_id)
        if not book:
            ExceptionService.raise_not_found("Book not found.")

        # به‌روزرسانی در پایگاه داده
        updated_book = self.book_repository.update_book(book_id, book_data)

        # به‌روزرسانی در Redis
        self.redis_repository.update_book(book_id, book_data.dict(exclude_unset=True))

        return updated_book
