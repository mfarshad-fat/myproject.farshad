from pydantic import BaseModel, validator
from typing import Optional

class TransactionsBase(BaseModel) :
    reservation_id :int
    transaction_type :str
    transaction_date :str
    librarian_id :int

    @validator('transaction_type')
    def check_role(cls, value):
        if value not in ['reserved', 'checked_out' , 'returned' , 'cancelled']:
            raise ValueError('role must be either "reserved" or "checked_out" or "returned" or "cancelled"')
        return value 


class TransactionsOut(TransactionsBase):
    transaction_id : int

class TransactionsUpdate(BaseModel) :
    reservation_id :Optional[int] = None
    transaction_type :str
    transaction_date :Optional[str] = None
    librarian_id :Optional[int] = None

    @validator('transaction_type')
    def check_role(cls, value):
        if value not in ['reserved', 'checked_out' , 'returned' , 'cancelled']:
            raise ValueError('role must be either "reserved" or "checked_out" or "returned" or "cancelled"')
        return value 