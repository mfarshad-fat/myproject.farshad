from src.allocation.adapters.repositories.books.redis_repository import RedisRepository
from src.allocation.adapters.repositories.books.postgres_repository import BookRepository
from src.allocation.service_layer.helpers.exception_service import ExceptionService

class DeleteBookService:
    def __init__(self, book_repository: BookRepository, redis_repository: RedisRepository):
        self.book_repository = book_repository
        self.redis_repository = redis_repository

    def execute(self, book_id: int):
        # بررسی وجود کتاب
        book = self.book_repository.get_by_id(book_id)
        if not book:
            ExceptionService.raise_not_found("Book not found.")

        # حذف از پایگاه داده
        self.book_repository.delete_book(book_id)

        # حذف از Redis
        self.redis_repository.delete_book(book_id)

        return {"detail": "Book deleted successfully"}
