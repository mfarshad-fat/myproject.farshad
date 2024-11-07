 
# entrypoint/routes/librarians.py

from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.orm import Session
import src.allocation.service_layer.helpers.jwt_auth as jwt
from src.allocation.adapters.orm.database import get_db
from src.allocation.adapters.dtos import LibrariansOut, LibrariansBase, LibrariansUpdate
import src.allocation.domain.entities as models
from src.allocation.adapters.dtos.userjwt_schemas import TokenData

router = APIRouter()

@router.get("/", response_model=list[LibrariansOut])
def read_librarians(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    librarians = db.query(models.Librarians).offset(skip).limit(limit).all()
    return librarians

@router.post("/", response_model=LibrariansBase)
def create_librarian(librarian: LibrariansBase, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_librarian = db.query(models.Librarians).filter(models.Librarians.email == librarian.email).first()
    if db_librarian:
        raise HTTPException(status_code=400, detail="Librarian already registered")
    new_librarian = models.Librarians(**librarian.dict())
    db.add(new_librarian)
    db.commit()
    db.refresh(new_librarian)
    return new_librarian

@router.put("/{librarian_id}", response_model=LibrariansOut)
def update_librarian(librarian_id: int, librarian: LibrariansUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_librarian = db.query(models.Librarians).filter(models.Librarians.librarian_id == librarian_id).first()
    if not db_librarian:
        raise HTTPException(status_code=404, detail="Librarian not found")
    for key, value in librarian.dict(exclude_unset=True).items():
        setattr(db_librarian, key, value)
    db.commit()
    db.refresh(db_librarian)
    return db_librarian

@router.delete("/{librarian_id}")
def delete_librarian(librarian_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_librarian = db.query(models.Librarians).filter(models.Librarians.librarian_id == librarian_id).first()
    if not db_librarian:
        raise HTTPException(status_code=404, detail="Librarian not found")
    db.delete(db_librarian)
    db.commit()
    return {"detail": "Librarian deleted successfully"}
