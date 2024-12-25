from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, Request
from sqlalchemy.orm import Session
from src.allocation.adapters.connector.postgres import get_db
from src.allocation.adapters.connector.redis import redis_client
from src.allocation.domain.entities import BooksBase, BooksOut
from src.allocation.service_layer.service.get_book import GetBooksService
from src.allocation.service_layer.service.create_book import CreateBookService
from src.allocation.service_layer.service.update_book import UpdateBookService
from src.allocation.service_layer.service.delete_book import DeleteBookService
from src.allocation.adapters.repositories.books.postgres_repository import BookRepository
from src.allocation.adapters.repositories.books.redis_repository import RedisRepository
from src.allocation.service_layer.helpers.client_ip_service import ClientIPService
from src.allocation.service_layer.helpers.dependencies_service import DependencyService

router = APIRouter()

@router.get("/", response_model=list[BooksOut])
async def read_books(
    skip: int = 0,
    limit: int = 10,
    title: str = None,
    sort_by: str = None,
    order: str = "asc",
    dependency_service: DependencyService = Depends(DependencyService)
):
    client_ip_service = ClientIPService(dependency_service.request)
    client_ip_service.check_rate_limit()

    redis_repository = RedisRepository(redis_client)
    get_books_service = GetBooksService(redis_repository)

    return get_books_service.execute(
        skip=skip, limit=limit, title=title, sort_by=sort_by, order=order
    )

@router.post("/", response_model=BooksOut)
def create_book(
    book: BooksBase,
    dependency_service: DependencyService = Depends(DependencyService)
):
    client_ip_service = ClientIPService(dependency_service.request)
    client_ip_service.check_rate_limit()

    book_repository = BookRepository(dependency_service.db)
    redis_repository = RedisRepository(redis_client)
    create_book_service = CreateBookService(book_repository, redis_repository)
    
    return create_book_service.execute(book_data=book)



@router.put("/{book_id}", response_model=BooksOut)
def update_book(
    book_id: int,
    book: BooksBase,
    dependency_service: DependencyService = Depends(DependencyService)
):
    client_ip_service = ClientIPService(dependency_service.request)
    client_ip_service.check_rate_limit()

    book_repository = BookRepository(dependency_service.db)
    redis_repository = RedisRepository(redis_client)
    update_book_service = UpdateBookService(book_repository, redis_repository)

    return update_book_service.execute(book_id=book_id, book_data=book)


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    dependency_service: DependencyService = Depends(DependencyService)
):
    client_ip_service = ClientIPService(dependency_service.request)
    client_ip_service.check_rate_limit()

    book_repository = BookRepository(dependency_service.db)
    redis_repository = RedisRepository(redis_client)
    delete_book_service = DeleteBookService(book_repository, redis_repository)

    return delete_book_service.execute(book_id=book_id)
