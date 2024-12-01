from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime , Boolean
from sqlalchemy.orm import relationship
from src.allocation.adapters.connector.postgres import Base

class Userjwt(Base):
    __tablename__ = "userjwt"
    
    userjwt_id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(VARCHAR , nullable=False)
    lastname = Column(VARCHAR , nullable=False)
    username = Column(VARCHAR, unique=True, nullable=False)
    access_id = Column(Integer, ForeignKey("acceclevel.access_id"))
    creat_at = Column (DateTime(timezone=True))
    is_logged_out = Column(Boolean, default=False)  # نشان می‌دهد کاربر logout شده است
    otp = Column(VARCHAR, default="None")
    otp_time = Column(DateTime(timezone=True), nullable=True)
    otp_time_expire = Column(DateTime(timezone=True), nullable=True)
    otp1 = Column(VARCHAR, default="None")
    otp1_time = Column(DateTime(timezone=True), nullable=True)
    otp1_time_expire = Column(DateTime(timezone=True), nullable=True)

    accec3_owner = relationship("AccessLevel", back_populates="accec_rell_3")
