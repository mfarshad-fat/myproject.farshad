from pydantic import BaseModel
from typing import Optional

class LibrariansBase(BaseModel) :
    first_name :str
    last_name :str
    email :str
    phone_number :str

class LibrariansOut(LibrariansBase):  # برای GET
    librarian_id: int

class LibrariansUpdate(BaseModel) : # مدل جدید برای PUT
    first_name :Optional[str] = None
    last_name :Optional[str] = None
    email :Optional[str] = None
    phone_number :Optional[str] = None
