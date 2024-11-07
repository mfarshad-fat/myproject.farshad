  
# bootstrap.py
from src.allocation.domain.entities import *
from src.allocation.adapters.orm.database import engine , Base


def init_db():
    # ایجاد تمام جداول در پایگاه داده با استفاده از `Base.metadata`
    Base.metadata.create_all(bind=engine)
