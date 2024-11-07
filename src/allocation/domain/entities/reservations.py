from sqlalchemy import Column, Integer, VARCHAR , DATE , ForeignKey
from sqlalchemy.orm import relationship
from src.allocation.adapters.orm.database import Base

class Reservations (Base) :
    __tablename__ = "reservations"
    
    reservation_id =Column(Integer , primary_key=True , nullable=False)
    user_id =Column(Integer , ForeignKey("users.user_id"))
    book_id = Column (Integer , ForeignKey("books.book_id"))
    reservation_date = Column(DATE)
    due_date = Column(DATE ,index=True)
    return_date = Column(DATE , index=True)
    status = Column(VARCHAR,index=True,server_default="reserved")

    user_owner = relationship("Users",back_populates="user_rell")
    book_owner = relationship("Books",back_populates="book_rell")

    reserv_rell=relationship("Transactions",back_populates="reserv_owner")