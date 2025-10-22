"""
NFT schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class NFTCreate(BaseModel):
    user_id: int
    metadata: Dict[str, Any]
    owner_address: Optional[str] = None

class NFTResponse(BaseModel):
    id: int
    owner_id: int
    token_id: Optional[str]
    metadata: Optional[Dict[str, Any]]
    on_chain: bool
    price: Optional[str]
    is_listed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class NFTListRequest(BaseModel):
    user_id: int
    price: str
    description: Optional[str] = None

class NFTBuyRequest(BaseModel):
    buyer_id: int
    nft_id: int
    payment_method: str = "internal"
