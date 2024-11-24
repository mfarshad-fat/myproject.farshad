# entrypoint/routes/userjwt.py

from fastapi import APIRouter, Depends, HTTPException, status , Query
from sqlalchemy.orm import Session
from src.allocation.adapters.connector.postgres import get_db
from src.allocation.domain.entities import UserjwtBase, Userjwtread , UserjwtUpdate
import src.allocation.adapters.models as models
import src.allocation.adapters.repositories as repo
import src.allocation.entrypoint.routes.login as login
import src.allocation.service_layer.helpers.jwt_auth as jwt
from datetime import timedelta
import random , string
from datetime import datetime, timedelta , timezone


router = APIRouter()
API_KEY = "1234"

def validate_key(key: str = Query(...)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    


#01
@router.get("/", response_model=list[Userjwtread])
def read_userjwt(key: str = Depends(validate_key),db: Session = Depends(get_db)):
    users_jwt = db.query(models.Userjwt).all()
    return users_jwt

#02
@router.post("/", response_model=Userjwtread)
def create_userjwt(user: UserjwtBase, key: str = Depends(validate_key), db: Session = Depends(get_db)):
    db_user = db.query(models.Userjwt).filter(models.Userjwt.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # hashed_password = jwt.get_password_hash(user.password)  # هش کردن پسورد
    new_user = models.Userjwt(username=user.username, firstname=user.firstname,lastname=user.lastname,access_id=user.access_id)    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#03
@router.put("/{jwt_id}", response_model=Userjwtread)
def update_userjwt(jwt_id: int, user: UserjwtUpdate, key: str = Depends(validate_key), db: Session = Depends(get_db)):
    db_user = db.query(models.Userjwt).filter(models.Userjwt.userjwt_id == jwt_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

#04
@router.delete("/{jwt_id}")
def delete_userjwt(jwt_id: int,key: str = Depends(validate_key), db: Session = Depends(get_db)):
    db_user = db.query(models.Userjwt).filter(models.Userjwt.userjwt_id == jwt_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}

#05
@router.post("/getOTP")
def getOTP(username: str, db: Session = Depends(get_db)):
    db_jwt = db.query(models.Userjwt).filter(models.Userjwt.username == username).first()
    if not db_jwt:
        raise HTTPException(status_code=404, detail="User not found")

    # تولید کد OTP تصادفی
    otp_code = ''.join(random.choices(string.digits, k=6))
    otp_time=datetime.now(timezone.utc)
    # ذخیره کد OTP در پایگاه داده
    db_jwt.otp = jwt.get_password_hash(otp_code)
    db_jwt.otp_time = otp_time
    expiry_minutes = 2 #مدت زمان انقضا
    otp_time += timedelta(minutes=expiry_minutes) 
    db_jwt.otp_time_expire = otp_time
    db.commit()
    db.refresh(db_jwt)
    return {"username": db_jwt.username, "otp": otp_code}
#06
@router.post("/logout-user")
async def admin_logout_user(username: str, key: str = Depends(validate_key) ,  db: Session = Depends(get_db)):
    user_repo = repo.UserRepository(db)
    success = user_repo.set_user_logged_out(username)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": f"User {username} has been logged out successfully"}






#06
# @router.post("/change_password")
# def change_password(username: str, new_password: str, otp: str, db: Session = Depends(get_db)):
#     db_user = db.query(models.Userjwt).filter(
#         models.Userjwt.username == username,
#         models.Userjwt.otp == otp ).first()
    
#     if not db_user:
#         raise HTTPException(status_code=400, detail="Invalid username or OTP")

#     current_time = datetime.now(timezone.utc)
#     if current_time > db_user.otp_time_expire :
#         db_user.otp = "None"
#         raise HTTPException(status_code=400, detail="OTP has expired")

#     hashed_password = jwt.get_password_hash(new_password)  # هش کردن پسورد

#     # به‌روزرسانی رمز عبور و خالی کردن فیلد OTP
#     db_user.password = hashed_password
#     db_user.otp = "None"  # پاک کردن کد OTP
#     db.commit()
#     db.refresh(db_user)
    
#     return {"detail": "Password changed successfully"}