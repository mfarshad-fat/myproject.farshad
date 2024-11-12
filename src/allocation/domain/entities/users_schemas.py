from pydantic import BaseModel, validator
from typing import Optional

class UsersBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    role: str
    access_id: int
    active: bool = True

    @validator("role")
    def check_role(cls, value):
        if value not in ["student", "faculty", "staff"]:
            raise ValueError('Role must be "student", "faculty", or "staff"')
        return value

    class Config:
        orm_mode = True

class UsersOut(UsersBase):
    user_id: int

class UsersUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    role: str
    active: Optional[bool] = None

    @validator("role")
    def check_role(cls, value):
        if value not in ["student", "faculty", "staff"]:
            raise ValueError('Role must be "student", "faculty", or "staff"')
        return value