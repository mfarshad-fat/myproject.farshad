# service_layer/helpers/jwt_auth.py

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException , Request , status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.allocation.domain.entities import TokenData
from sqlalchemy.orm import Session
from src.allocation.adapters.connector.postgres import get_db
from src.allocation.adapters.repositories import UserRepository



# تنظیمات JWT
SECRET_KEY = "sadljgojsdofjSBGSsaasfaAVa65484sdsdf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 50

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["argon2", "sha256_crypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request ,token: str = Depends(oauth2_scheme) , db: Session = Depends(get_db)) :
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        # Check if the user is logged out
        if user.is_logged_out:
            raise HTTPException(
                status_code=403,
                detail="User has been logged out",
            )

        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token")

# async def get_current_user(request: Request ,token: str = Depends(oauth2_scheme) , db: Session = Depends(get_db)) :
    
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
        
#         user_repo = UserRepository(db)
#         user = user_repo.get_user_by_username(username)
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="User not found",
#             )
#         # Check if the user is logged out
#         if user.is_logged_out:
#             raise HTTPException(
#                 status_code=403,
#                 detail="User has been logged out",
#             )

#         return user
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token")