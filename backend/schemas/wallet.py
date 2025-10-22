"""
Wallet schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict
from decimal import Decimal
from datetime import datetime

class WalletCreate(BaseModel):
    user_id: int
    asset: str
    address: str

class WalletResponse(BaseModel):
    id: int
    user_id: int
    asset: str
    address: str
    type: str
    is_active: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BalanceResponse(BaseModel):
    user_id: int
    asset: str
    amount: Decimal
    reserved: Decimal
    available: Decimal
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DepositRequest(BaseModel):
    user_id: int
    asset: str
    amount: Decimal

class WithdrawRequest(BaseModel):
    user_id: int
    asset: str
    amount: Decimal
    to_address: str

class TransferRequest(BaseModel):
    from_user_id: int
    to_user_id: int
    asset: str
    amount: Decimal
