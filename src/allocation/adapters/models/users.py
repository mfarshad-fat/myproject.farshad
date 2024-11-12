from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.allocation.adapters.connector.database import Base

class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(VARCHAR, index=True)
    last_name = Column(VARCHAR, index=True)
    email = Column(VARCHAR, unique=True, index=True)
    phone_number = Column(VARCHAR, unique=True, index=True)
    role = Column(VARCHAR)
    active = Column(Boolean, server_default='true')
    
    access_id = Column(Integer, ForeignKey("acceclevel.access_id"))
    accec2_owner = relationship("AccessLevel", back_populates="accec_rell_2")

    user_rell = relationship("Reservations", back_populates="user_owner")
