"""
Balance model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from database import Base

class Balance(Base):
    __tablename__ = "balances"
    
    user_id = Column(Integer, primary_key=True, index=True)
    asset = Column(String(10), primary_key=True, index=True)
    amount = Column(Numeric(20, 8), default=0)  # Total balance
    reserved = Column(Numeric(20, 8), default=0)  # Reserved for orders
    available = Column(Numeric(20, 8), default=0)  # Available = amount - reserved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Balance(user_id={self.user_id}, asset={self.asset}, amount={self.amount}, available={self.available})>"
