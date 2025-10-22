"""
Wallet model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class WalletType(enum.Enum):
    CUSTODIAL = "custodial"
    EXTERNAL = "external"

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    asset = Column(String(10), nullable=False)  # BTC, ETH, USDT, etc.
    address = Column(String(255), nullable=False)
    type = Column(Enum(WalletType), default=WalletType.CUSTODIAL)
    is_active = Column(String(1), default="Y")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Wallet(id={self.id}, user_id={self.user_id}, asset={self.asset}, address={self.address})>"
