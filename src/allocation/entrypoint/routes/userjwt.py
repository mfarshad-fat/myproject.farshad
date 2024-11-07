# entrypoint/routes/userjwt.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.allocation.adapters.orm.database import get_db
from src.allocation.adapters.dtos.userjwt_schemas import UserjwtBase, Userjwtread
import src.allocation.domain.entities as models
from fastapi.security import OAuth2PasswordRequestForm
import src.allocation.service_layer.helpers.jwt_auth as jwt
from datetime import timedelta

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Userjwt).filter(models.Userjwt.username == form_data.username).first()
    if not user or not jwt.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=list[Userjwtread])
def read_userjwt(db: Session = Depends(get_db)):
    users_jwt = db.query(models.Userjwt).all()
    return users_jwt

@router.post("/", response_model=Userjwtread)
def create_userjwt(user: UserjwtBase, db: Session = Depends(get_db)):
    db_user = db.query(models.Userjwt).filter(models.Userjwt.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = jwt.get_password_hash(user.password)  # هش کردن پسورد
    new_user = models.Userjwt(username=user.username, password=hashed_password, access_id=user.access_id)    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{jwt_id}", response_model=Userjwtread)
def update_userjwt(jwt_id: int, user: UserjwtBase, db: Session = Depends(get_db)):
    db_user = db.query(models.Userjwt).filter(models.Userjwt.jwt_id == jwt_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.username = user.username
    db_user.password = jwt.get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{jwt_id}")
def delete_userjwt(jwt_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Userjwt).filter(models.Userjwt.jwt_id == jwt_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
