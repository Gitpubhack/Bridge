"""
Invoice model for Bridge Exchange (CryptoPay integration)
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, JSON, Enum
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.sql import func
from database import Base
import enum

class InvoiceStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    provider_invoice_id = Column(String(255), unique=True, nullable=False)  # CryptoPay invoice ID
    asset = Column(String(10), nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.PENDING)
    pay_url = Column(Text, nullable=True)
    raw_data = Column(JSON, nullable=True)  # Raw response from CryptoPay
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, user_id={self.user_id}, asset={self.asset}, amount={self.amount}, status={self.status})>"
