  
# bootstrap.py
from src.allocation.domain.entities import *
from src.allocation.adapters.connector.postgres import engine , Base
from sqlalchemy import create_engine

def init_db():
    # ایجاد تمام جداول در پایگاه داده با استفاده از `Base.metadata`
    Base.metadata.create_all(bind=engine)
