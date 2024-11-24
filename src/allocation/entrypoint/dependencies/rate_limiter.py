from time import time
from src.allocation.adapters.connector.redis import redis_client

LIMIT = 3  # حداکثر تعداد درخواست‌ها
WINDOW = 60  # بازه زمانی به ثانیه (مثلاً 60 ثانیه)
value = True


class RateLimiter:
    def __init__(self, limit=LIMIT, window=WINDOW):
        self.redis_client = redis_client
        self.limit = limit
        self.window = window
    
    def is_rate_limited(self, client_id: str) -> bool:
        current_time = int(time())
        key = f"rate_limit:{client_id}"

        # تعداد درخواست‌های ذخیره‌شده در بازه
        request_count = self.redis_client.zcount(key, current_time - self.window, current_time)

        if request_count >= self.limit:
            return True

        # اضافه کردن زمان درخواست جدید
        self.redis_client.zadd(key, {str(current_time): current_time})
        self.redis_client.expire(key, self.window)
        return False