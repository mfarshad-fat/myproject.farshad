import redis
from typing import Any, Dict, List, Optional

class RedisRepository:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def get_all_books(self) -> List[Dict[str, Any]]:
        book_keys = self.redis_client.lrange("books", 0, -1)
        books = []
        for book_key in book_keys:
            book_info = self.redis_client.hgetall(book_key)
            books.append({k: v for k, v in book_info.items()})
        return books

    def save_book(self, book_id: int, book_data: Dict[str, Any]) -> None:
        book_key = f"book:{book_id}"
        self.redis_client.hset(book_key, mapping=book_data)
        self.redis_client.rpush("books", book_key)

    def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        book_key = f"book:{book_id}"
        book_info = self.redis_client.hgetall(book_key)
        if not book_info:
            return None
        return {k.decode("utf-8"): v.decode("utf-8") for k, v in book_info.items()}

    def delete_book(self, book_id: int) -> None:
        book_key = f"book:{book_id}"
        self.redis_client.delete(book_key)
        self.redis_client.lrem("books", 0, book_key)

    def update_book(self, book_id: int, updated_data: Dict[str, Any]) -> None:
        book_key = f"book:{book_id}"
        self.redis_client.hset(book_key, mapping=updated_data)
