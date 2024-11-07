 
# entrypoint/routes/reservations.py

from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.orm import Session
import src.allocation.service_layer.helpers.jwt_auth as jwt
from src.allocation.adapters.orm.database import get_db
from src.allocation.adapters.dtos import ReservationsOut, ReservationsBase, ReservationsUpdate
import src.allocation.domain.entities as models
from src.allocation.adapters.dtos.userjwt_schemas import TokenData

router = APIRouter()

@router.get("/", response_model=list[ReservationsOut])
def read_reservations(db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    reservations = db.query(models.Reservations).all()
    return reservations

@router.post("/", response_model=ReservationsBase)
def create_reservation(reservation: ReservationsBase, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    new_reservation = models.Reservations(**reservation.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

@router.put("/{reservation_id}", response_model=ReservationsOut)
def update_reservation(reservation_id: int, reservation: ReservationsUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_reservation = db.query(models.Reservations).filter(models.Reservations.reservation_id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    for key, value in reservation.dict(exclude_unset=True).items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(jwt.get_current_user)):
    db_reservation = db.query(models.Reservations).filter(models.Reservations.reservation_id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return {"detail": "Reservation deleted successfully"}
