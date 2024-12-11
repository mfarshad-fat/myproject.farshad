from fastapi import HTTPException

class ExceptionService:
    @staticmethod
    def raise_not_found(detail: str = "Resource not found"):
        raise HTTPException(status_code=404, detail=detail)

    @staticmethod
    def raise_bad_request(detail: str = "Bad request"):
        raise HTTPException(status_code=400, detail=detail)

    @staticmethod
    def raise_rate_limit():
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
