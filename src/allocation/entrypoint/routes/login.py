from fastapi import APIRouter, Depends, HTTPException, status , Query , Response
from fastapi.security import OAuth2PasswordRequestForm
from src.allocation.adapters.connector.postgres import get_db
from sqlalchemy.orm import Session
import src.allocation.adapters.models as models
import src.allocation.service_layer.helpers.jwt_auth as jwt
from datetime import timedelta , timezone , datetime

router = APIRouter()


@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Userjwt).filter(models.Userjwt.username == form_data.username).first()
    current_time = datetime.now(timezone.utc)

    if not user or not jwt.verify_password(form_data.password, user.otp) or current_time > user.otp_time_expire :
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or OTP",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.otp = "None"
    user.is_logged_out = False
    db.commit()
    db.refresh(user)
    
    access_token_expires = timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    # response = Response(content="Login successful")
    # response.set_cookie(
    #     key="access_token", 
    #     value=access_token, 
    #     httponly=True,  # جلوگیری از دسترسی به کوکی از سمت جاوااسکریپت
    #     max_age=60 * 30,  # مدت اعتبار کوکی به ثانیه (مثلاً 30 دقیقه)
    #     secure=True,  # فقط روی HTTPS فعال شود
    # )

    return {"access_token": access_token, "token_type": "bearer"}