from pydantic import BaseModel, validator
from typing import Optional

class ReservationsBase(BaseModel) :
    user_id :int
    book_id :int
    reservation_date :str
    due_date :str
    return_date :str
    status :str

    @validator('status')
    def check_role(cls, value):
        if value not in ['reserved', 'checked_out' , 'returned' , 'cancelled']:
            raise ValueError('role must be either "reserved" or "checked_out" or "returned" or "cancelled"')
        return value    

class ReservationsOut(ReservationsBase):
    reservation_id : int

class ReservationsUpdate(BaseModel) : # مدل جدید برای PUT
    user_id :Optional[int] = None
    book_id :Optional[int] = None
    reservation_date :Optional[str] = None
    due_date :Optional[str] = None
    return_date :Optional[str] = None
    status :Optional[str] = None