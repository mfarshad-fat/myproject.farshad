from src.allocation.adapters.repositories.books.redis_repository import RedisRepository
from src.allocation.adapters.repositories.books.postgres_repository import BookRepository
from src.allocation.domain.entities import BooksBase
from src.allocation.service_layer.helpers.exception_service import ExceptionService

class CreateBookService:
    def __init__(self, book_repository: BookRepository, redis_repository: RedisRepository):
        self.book_repository = book_repository
        self.redis_repository = redis_repository

    def execute(self, book_data: BooksBase):
        # بررسی وجود کتاب در پایگاه داده
        existing_book = self.book_repository.get_book_by_isbn(book_data.isbn)
        if existing_book:
            ExceptionService.raise_bad_request("Book with this ISBN already exists.")

        new_book = self.book_repository.create_book(book_data)

        # ذخیره در Redis
        book_dict = book_data.dict()
        book_dict["book_id"] = new_book.book_id
        self.redis_repository.save_book(new_book.book_id, book_dict)

        return new_book
