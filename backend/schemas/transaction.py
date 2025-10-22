"""
Transaction schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from decimal import Decimal
from datetime import datetime
from models.transaction import TransactionType, TransactionStatus

class TransactionCreate(BaseModel):
    user_id: int
    type: TransactionType
    amount: Decimal
    asset: str
    fee: Optional[Decimal] = 0
    meta: Optional[Dict[str, Any]] = None
    tx_hash: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    amount: Decimal
    asset: str
    status: TransactionStatus
    fee: Decimal
    meta: Optional[Dict[str, Any]]
    tx_hash: Optional[str]
    from_address: Optional[str]
    to_address: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
