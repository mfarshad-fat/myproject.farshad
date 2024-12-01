from time import time
from src.allocation.adapters.connector.redis import redis_client

MINUTE_LIMIT = 5  # حداکثر تعداد درخواست‌ها در هر دقیقه
HOUR_LIMIT = 10   # حداکثر تعداد درخواست‌ها در هر ساعت
MINUTE_WINDOW = 120 # بازه زمانی به ثانیه (2 دقیقه)
HOUR_WINDOW = 3600  # بازه زمانی به ثانیه (1 ساعت)
class RateLimiter:
    def __init__(self, minute_limit=MINUTE_LIMIT, hour_limit=HOUR_LIMIT, minute_window=MINUTE_WINDOW, hour_window=HOUR_WINDOW):
        self.redis_client = redis_client
        self.minute_limit = minute_limit
        self.hour_limit = hour_limit
        self.minute_window = minute_window
        self.hour_window = hour_window
    
    def is_rate_limited(self, client_id: str) -> bool:
        current_time = int(time())
        
        # کلید برای محدودیت ۱ دقیقه
        minute_key = f"rate_limit:minute:{client_id}"
        # کلید برای محدودیت ۱ ساعت
        hour_key = f"rate_limit:hour:{client_id}"

        # تعداد درخواست‌های ذخیره‌شده در بازه زمانی ۱ دقیقه
        minute_request_count = self.redis_client.zcount(minute_key, current_time - self.minute_window, current_time)
        
        if minute_request_count >= self.minute_limit:
            return True
        
        # تعداد درخواست‌های ذخیره‌شده در بازه زمانی ۱ ساعت
        hour_request_count = self.redis_client.zcount(hour_key, current_time - self.hour_window, current_time)
        if hour_request_count >= self.hour_limit:
            return True

        # اضافه کردن زمان درخواست جدید به کلید ۱ دقیقه
        self.redis_client.zadd(minute_key, {str(current_time): current_time})
        self.redis_client.expire(minute_key, self.minute_window)

        # اضافه کردن زمان درخواست جدید به کلید ۱ ساعت
        self.redis_client.zadd(hour_key, {str(current_time): current_time})
        self.redis_client.expire(hour_key, self.hour_window)

        return False
