from sqlalchemy import Column, Integer, VARCHAR , ForeignKey
from sqlalchemy.orm import relationship
from src.allocation.adapters.connector.postgres import Base

class Books (Base) :
    __tablename__="books"

    book_id=Column(Integer,primary_key=True,nullable=False)
    title=Column(VARCHAR,nullable=False)
    author=Column(VARCHAR,index=True)
    isbn=Column(VARCHAR,index=True,unique=True)  #shaparak
    published_year=Column(Integer,index=True)
    genre=Column(VARCHAR,index=True)
    total_copies=Column(Integer)
    price=Column(VARCHAR,index=True)
    access_id=Column(Integer,ForeignKey("acceclevel.access_id"))
    accec1_owner=relationship("AccessLevel",back_populates="accec_rell_1")

    book_rell = relationship("Reservations",back_populates="book_owner")