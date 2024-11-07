from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TokenData(BaseModel):
    username: Optional[str] = None

class UserjwtBase(BaseModel) :
    username: str
    password: str
    access_id : int
    class Config:
        orm_mode = True

class Userjwtread(UserjwtBase) :
    jwt_id : int
    otp : str
    otp_time : Optional[datetime] = None
    otp_time_expire : Optional[datetime] = None