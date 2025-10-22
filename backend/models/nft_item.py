"""
NFT Item model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text
from sqlalchemy.sql import func
from database import Base

class NFTItem(Base):
    __tablename__ = "nft_items"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False, index=True)
    token_id = Column(String(255), nullable=True)  # On-chain token ID
    nft_metadata = Column(JSON, nullable=True)  # NFT metadata
    on_chain = Column(Boolean, default=False)  # Whether minted on blockchain
    price = Column(String(20), nullable=True)  # Sale price if listed
    is_listed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<NFTItem(id={self.id}, owner_id={self.owner_id}, token_id={self.token_id}, on_chain={self.on_chain})>"
