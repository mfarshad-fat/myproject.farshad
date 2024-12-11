from fastapi import HTTPException
from src.allocation.entrypoint.dependencies.rate_limiter import RateLimiter

class ClientIPService:
    def __init__(self, request):
        self.client_ip = request.client.host
        self.rate_limiter = RateLimiter()

    def check_rate_limit(self):
        if self.rate_limiter.is_rate_limited(self.client_ip):
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
