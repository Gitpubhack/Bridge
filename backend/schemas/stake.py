"""
Staking schemas
"""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime, timedelta

class StakeCreate(BaseModel):
    user_id: int
    asset: str
    amount: Decimal
    duration_days: int = 30  # Default 30 days

class StakeResponse(BaseModel):
    id: int
    user_id: int
    asset: str
    amount: Decimal
    apr: Decimal
    since: datetime
    until: datetime
    is_active: bool
    rewards_claimed: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True

class UnstakeRequest(BaseModel):
    user_id: int
    stake_id: int

class ClaimRewardsRequest(BaseModel):
    user_id: int
    stake_id: int
