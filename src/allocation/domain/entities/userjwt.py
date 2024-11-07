from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.allocation.adapters.orm.database import Base

class Userjwt(Base):
    __tablename__ = "userjwt"
    
    jwt_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(VARCHAR, unique=True, nullable=False)
    password = Column(VARCHAR, nullable=False)
    access_id = Column(Integer, ForeignKey("acceclevel.access_id"))
    otp = Column(VARCHAR, default="None")
    otp_time = Column(DateTime(timezone=True), nullable=True)
    otp_time_expire = Column(DateTime(timezone=True), nullable=True)

    accec3_owner = relationship("AccessLevel", back_populates="accec_rell_3")
