from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TokenData(BaseModel):
    username: Optional[str] = None

class UserjwtBase(BaseModel) :
    firstname: str
    lastname: str
    username: str
    access_id : int
    pr_account : bool = False
    class Config:
        orm_mode = True

class Userjwtread(UserjwtBase) :
    userjwt_id : int
    creat_at : Optional[datetime] = None
    is_logged_out : Optional[bool] = None
    otp : Optional[str] = None
    otp_time : Optional[datetime] = None
    otp_time_expire : Optional[datetime] = None
    otp1 : Optional[str] = None
    otp1_time : Optional[datetime] = None
    otp1_time_expire : Optional[datetime] = None


class UserjwtUpdate(BaseModel) :
    firstname : Optional[str] = None
    lastname : Optional[str] = None
    username : Optional[str] = None
    access_id : Optional[int] = None
