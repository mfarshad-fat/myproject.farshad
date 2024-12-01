from sqlalchemy import Column, Integer, VARCHAR , DATE , ForeignKey
from sqlalchemy.orm import relationship
from src.allocation.adapters.connector.postgres import Base

class Transactions (Base) :
    __tablename__ = "transactions"
    
    transaction_id =Column(Integer,primary_key = True,nullable=False)
    reservation_id =Column(Integer, ForeignKey("reservations.reservation_id"))
    transaction_type = Column (VARCHAR,index=True)
    transaction_date = Column (DATE,index=True)
    reserv_owner = relationship("Reservations",back_populates="reserv_rell")