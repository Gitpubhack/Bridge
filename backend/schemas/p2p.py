"""
P2P schemas
"""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from models.p2p_offer import P2PStatus

class P2POfferCreate(BaseModel):
    seller_id: int
    asset: str
    amount: Decimal
    price: Decimal
    payment_method: str
    description: Optional[str] = None

class P2POfferResponse(BaseModel):
    id: int
    seller_id: int
    buyer_id: Optional[int]
    asset: str
    amount: Decimal
    price: Decimal
    payment_method: str
    status: P2PStatus
    escrow_tx: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class P2PAcceptRequest(BaseModel):
    buyer_id: int
    offer_id: int

class P2PReleaseRequest(BaseModel):
    user_id: int
    offer_id: int
    action: str  # "release" or "dispute"
