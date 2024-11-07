 
# entrypoint/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status , Query
from sqlalchemy.orm import Session
import src.allocation.service_layer.helpers.jwt_auth as jwt
from src.allocation.adapters.orm.database import get_db
from src.allocation.adapters.dtos import UsersOut, UsersBase, UsersUpdate
import src.allocation.domain.entities as models
from src.allocation.adapters.dtos.userjwt_schemas import TokenData
router = APIRouter()

@router.get("/", response_model=list[UsersOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    users = db.query(models.Users).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UsersBase)
def create_user(user: UsersBase, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=UsersOut)
def update_user(user_id: int, user: UsersUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
