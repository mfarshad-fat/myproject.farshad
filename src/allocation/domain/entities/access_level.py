from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from src.allocation.adapters.orm.database import Base

class AccessLevel(Base):
    __tablename__ = "acceclevel"
    
    access_id = Column(Integer, primary_key=True, nullable=False)
    accec_name = Column(VARCHAR, nullable=False)

    accec_rell_1 = relationship("Books", back_populates="accec1_owner")
    accec_rell_2 = relationship("Users", back_populates="accec2_owner")
    accec_rell_3 = relationship("Userjwt", back_populates="accec3_owner")
