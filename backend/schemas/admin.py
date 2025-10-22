"""
Admin schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from decimal import Decimal
from datetime import datetime

class AdminActionRequest(BaseModel):
    admin_id: int
    action: str
    target_user_id: Optional[int] = None
    description: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class AdjustBalanceRequest(BaseModel):
    admin_id: int
    user_id: int
    asset: str
    amount: Decimal
    reason: str

class FreezeUserRequest(BaseModel):
    admin_id: int
    user_id: int
    reason: str
    duration_hours: Optional[int] = None

class RefundRequest(BaseModel):
    admin_id: int
    transaction_id: int
    reason: str
    amount: Optional[Decimal] = None

class AdminLogResponse(BaseModel):
    id: int
    admin_id: int
    action: str
    target_user_id: Optional[int]
    description: Optional[str]
    meta: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class AdminStatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_volume_24h: Decimal
    pending_withdrawals: int
    open_tickets: int
    total_balance: Dict[str, Decimal]
