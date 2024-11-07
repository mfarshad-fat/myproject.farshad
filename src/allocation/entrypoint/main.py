# entrypoint/main.py

from fastapi import FastAPI
from src.allocation.service_layer.helpers.jwt_auth import *
from src.allocation.bootstrap import init_db
from src.allocation.adapters.dtos import *
from src.allocation.adapters.orm import database
from src.allocation.entrypoint.routes import users_router, books_router, reservations_router, transactions_router, librarians_router , userjwt_router
app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     init_db()

# تنظیم روت‌ها
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(books_router, prefix="/books", tags=["Books"])
app.include_router(reservations_router, prefix="/reservations", tags=["Reservations"])
app.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])
app.include_router(librarians_router, prefix="/librarians", tags=["Librarians"])
app.include_router(userjwt_router, prefix="/userjwt", tags=["UserJWT"])

