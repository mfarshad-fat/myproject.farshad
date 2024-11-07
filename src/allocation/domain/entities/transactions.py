from sqlalchemy import Column, Integer, VARCHAR , DATE , ForeignKey
from sqlalchemy.orm import relationship
from src.allocation.adapters.orm.database import Base

class Transactions (Base) :
    __tablename__ = "transactions"
    
    transaction_id =Column(Integer,primary_key = True,nullable=False)
    reservation_id =Column(Integer, ForeignKey("reservations.reservation_id"))
    transaction_type = Column (VARCHAR,index=True)
    transaction_date = Column (DATE,index=True)
    librarian_id = Column (Integer , ForeignKey("librarians.librarian_id"))

    reserv_owner = relationship("Reservations",back_populates="reserv_rell")
    librarian_owner=relationship("Librarians",back_populates="librarian_rell")