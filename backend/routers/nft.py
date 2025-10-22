"""
NFT router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any

from database import get_db
from models.nft_item import NFTItem
from schemas.nft import NFTCreate, NFTResponse, NFTListRequest, NFTBuyRequest
from services.ton import TONClient
from routers.auth import get_current_user

router = APIRouter()
ton_client = TONClient()

@router.post("/mint")
async def mint_nft(
    request: NFTCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Mint an NFT"""
    try:
        # Try to mint on TON blockchain
        mint_result = await ton_client.mint_nft(
            owner_address=request.owner_address or f"user_{current_user['id']}",
            metadata=request.metadata
        )
        
        if mint_result.get("ok"):
            # Create NFT record
            nft = NFTItem(
                owner_id=current_user["id"],
                token_id=mint_result["result"]["token_id"],
                metadata=request.metadata,
                on_chain=True
            )
        else:
            # Create off-chain NFT (admin will mint later)
            nft = NFTItem(
                owner_id=current_user["id"],
                metadata=request.metadata,
                on_chain=False
            )
        
        db.add(nft)
        await db.commit()
        await db.refresh(nft)
        
        return NFTResponse(
            id=nft.id,
            owner_id=nft.owner_id,
            token_id=nft.token_id,
            metadata=nft.metadata,
            on_chain=nft.on_chain,
            price=nft.price,
            is_listed=nft.is_listed,
            created_at=nft.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mint NFT"
        )

@router.get("/listings")
async def get_nft_listings(
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get NFT marketplace listings"""
    try:
        result = await db.execute(
            select(NFTItem)
            .where(NFTItem.is_listed == True)
            .limit(limit)
        )
        nfts = result.scalars().all()
        
        return [
            NFTResponse(
                id=nft.id,
                owner_id=nft.owner_id,
                token_id=nft.token_id,
                metadata=nft.metadata,
                on_chain=nft.on_chain,
                price=nft.price,
                is_listed=nft.is_listed,
                created_at=nft.created_at
            )
            for nft in nfts
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get listings"
        )

@router.post("/buy")
async def buy_nft(
    request: NFTBuyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Buy an NFT"""
    try:
        # Get NFT
        result = await db.execute(
            select(NFTItem).where(NFTItem.id == request.nft_id)
        )
        nft = result.scalar_one_or_none()
        
        if not nft:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="NFT not found"
            )
        
        if not nft.is_listed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="NFT not for sale"
            )
        
        # Transfer ownership
        nft.owner_id = request.buyer_id
        nft.is_listed = False
        nft.price = None
        
        await db.commit()
        
        return {"success": True, "nft_id": request.nft_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to buy NFT"
        )
