"""
Stake model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Stake(Base):
    __tablename__ = "stakes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    asset = Column(String(10), nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    apr = Column(Numeric(5, 2), nullable=False)  # Annual percentage rate
    since = Column(DateTime(timezone=True), nullable=False)
    until = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    rewards_claimed = Column(Numeric(20, 8), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Stake(id={self.id}, user_id={self.user_id}, asset={self.asset}, amount={self.amount}, apr={self.apr})>"
