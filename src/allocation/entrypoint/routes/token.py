from fastapi import APIRouter, Depends, HTTPException, status , Query
from fastapi.security import OAuth2PasswordRequestForm
from src.allocation.adapters.orm.database import get_db
from sqlalchemy.orm import Session
import src.allocation.domain.entities as models
import src.allocation.service_layer.helpers.jwt_auth as jwt
from datetime import timedelta



router = APIRouter()
@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Userjwt).filter(models.Userjwt.username == form_data.username).first()
    if not user or not jwt.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}