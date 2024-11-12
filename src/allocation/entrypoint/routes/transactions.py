 
# entrypoint/routes/transactions.py

from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.orm import Session
import src.allocation.service_layer.helpers.jwt_auth as jwt
from src.allocation.adapters.connector.database import get_db
from src.allocation.domain.entities import TransactionsOut, TransactionsBase, TransactionsUpdate
import src.allocation.adapters.models as models
from src.allocation.domain.entities.userjwt_schemas import TokenData

router = APIRouter()

@router.get("/", response_model=list[TransactionsOut])
def read_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    transactions = db.query(models.Transactions).offset(skip).limit(limit).all()
    return transactions

@router.post("/", response_model=TransactionsBase)
def create_transaction(transaction: TransactionsBase, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    reservation = db.query(models.Reservations).filter(models.Reservations.reservation_id == transaction.reservation_id).first()
    librarian = db.query(models.Librarians).filter(models.Librarians.librarian_id == transaction.librarian_id).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if not librarian:
        raise HTTPException(status_code=404, detail="Librarian not found")

    new_transaction = models.Transactions(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.put("/{transaction_id}", response_model=TransactionsOut)
def update_transaction(transaction_id: int, transaction: TransactionsUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_transaction = db.query(models.Transactions).filter(models.Transactions.transaction_id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_transaction = db.query(models.Transactions).filter(models.Transactions.transaction_id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully"}
