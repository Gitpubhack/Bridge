"""
User schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_premium: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    is_premium: bool
    level: int
    xp: int
    kyc_status: str
    is_active: bool
    is_admin: bool
    trading_commission: str
    referral_code: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
