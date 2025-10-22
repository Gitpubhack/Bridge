"""
P2P router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from database import get_db
from models.p2p_offer import P2POffer, P2PStatus
from schemas.p2p import P2POfferCreate, P2POfferResponse, P2PAcceptRequest, P2PReleaseRequest
from routers.auth import get_current_user

router = APIRouter()

@router.post("/offer")
async def create_p2p_offer(
    request: P2POfferCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create P2P offer"""
    try:
        # Reserve seller funds
        from routers.wallet import get_user_balance
        balance = await get_user_balance(db, current_user["id"], request.asset)
        
        if balance.available < request.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )
        
        # Reserve funds
        balance.reserved += request.amount
        balance.available = balance.amount - balance.reserved
        await db.commit()
        
        # Create offer
        offer = P2POffer(
            seller_id=current_user["id"],
            asset=request.asset,
            amount=request.amount,
            price=request.price,
            payment_method=request.payment_method,
            description=request.description,
            status=P2PStatus.ACTIVE
        )
        
        db.add(offer)
        await db.commit()
        await db.refresh(offer)
        
        return P2POfferResponse(
            id=offer.id,
            seller_id=offer.seller_id,
            buyer_id=offer.buyer_id,
            asset=offer.asset,
            amount=offer.amount,
            price=offer.price,
            payment_method=offer.payment_method,
            status=offer.status,
            escrow_tx=offer.escrow_tx,
            description=offer.description,
            created_at=offer.created_at,
            updated_at=offer.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create offer"
        )

@router.post("/accept")
async def accept_p2p_offer(
    request: P2PAcceptRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Accept P2P offer"""
    try:
        # Get offer
        result = await db.execute(
            select(P2POffer).where(P2POffer.id == request.offer_id)
        )
        offer = result.scalar_one_or_none()
        
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer not found"
            )
        
        if offer.status != P2PStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Offer not available"
            )
        
        # Update offer
        offer.buyer_id = request.buyer_id
        offer.status = P2PStatus.COMPLETED
        offer.escrow_tx = f"escrow_{offer.id}_{request.buyer_id}"
        
        await db.commit()
        
        return {"success": True, "offer_id": offer.id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to accept offer"
        )

@router.post("/release")
async def release_p2p_funds(
    request: P2PReleaseRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Release or dispute P2P funds"""
    try:
        # Get offer
        result = await db.execute(
            select(P2POffer).where(P2POffer.id == request.offer_id)
        )
        offer = result.scalar_one_or_none()
        
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer not found"
            )
        
        if request.action == "release":
            # Release funds to buyer
            from routers.wallet import update_balance
            await update_balance(db, offer.buyer_id, offer.asset, offer.amount)
            offer.status = P2PStatus.COMPLETED
        elif request.action == "dispute":
            # Create dispute
            offer.status = P2PStatus.DISPUTED
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid action"
            )
        
        await db.commit()
        
        return {"success": True, "action": request.action}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process request"
        )
