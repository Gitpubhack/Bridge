"""
Referral model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from database import Base

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, nullable=False, index=True)
    referred_id = Column(Integer, nullable=False, index=True)
    bonus_amount = Column(Numeric(20, 8), default=0)
    commission_rate = Column(String(10), default="0.1")  # Percentage as string
    status = Column(String(20), default="active")  # active, cancelled, paid
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Referral(id={self.id}, referrer_id={self.referrer_id}, referred_id={self.referred_id}, bonus_amount={self.bonus_amount})>"
