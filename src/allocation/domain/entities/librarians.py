from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from src.allocation.adapters.orm.database import Base

class Librarians (Base) :
    __tablename__ = "librarians"
    
    librarian_id =Column(Integer,primary_key = True,nullable=False)
    first_name =Column(VARCHAR,index=True)
    last_name = Column (VARCHAR,index=True)
    email = Column(VARCHAR,unique=True)
    phone_number = Column(VARCHAR,index=True,unique=True )

    librarian_rell=relationship("Transactions",back_populates="librarian_owner")