"""
P2P Offer model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, Text
from sqlalchemy.sql import func
from database import Base
import enum

class P2PStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"

class P2POffer(Base):
    __tablename__ = "p2p_offers"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, nullable=False, index=True)
    buyer_id = Column(Integer, nullable=True, index=True)
    asset = Column(String(10), nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    payment_method = Column(String(100), nullable=False)  # Bank transfer, PayPal, etc.
    status = Column(Enum(P2PStatus), default=P2PStatus.ACTIVE)
    escrow_tx = Column(String(255), nullable=True)  # Escrow transaction hash
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<P2POffer(id={self.id}, seller_id={self.seller_id}, asset={self.asset}, amount={self.amount}, status={self.status})>"
