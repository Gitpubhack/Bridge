"""
Transaction model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, JSON, Enum
from sqlalchemy.sql import func
import enum
from database import Base


class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRADE = "trade"
    P2P = "p2p"
    NFT = "nft"
    FEE = "fee"
    REWARD = "reward"
    REFUND = "refund"
    TRANSFER = "transfer"

class TransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    asset = Column(String(10), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    fee = Column(Numeric(20, 8), default=0)
    meta = Column(JSON, nullable=True)  # Additional transaction data
    tx_hash = Column(String(255), nullable=True)  # Blockchain transaction hash
    from_address = Column(String(255), nullable=True)
    to_address = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, type={self.type}, amount={self.amount}, asset={self.asset})>"
