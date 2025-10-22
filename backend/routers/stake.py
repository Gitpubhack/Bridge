"""
Staking router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal
from datetime import datetime, timedelta

from database import get_db
from models.stake import Stake
from schemas.stake import StakeCreate, StakeResponse, UnstakeRequest, ClaimRewardsRequest
from routers.auth import get_current_user

router = APIRouter()

@router.post("/stake")
async def create_stake(
    request: StakeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a stake"""
    try:
        # Check balance
        from routers.wallet import get_user_balance
        balance = await get_user_balance(db, current_user["id"], request.asset)
        
        if balance.available < request.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )
        
        # Calculate APR based on duration
        apr = Decimal("5.0") if request.duration_days >= 30 else Decimal("3.0")
        
        # Create stake
        stake = Stake(
            user_id=current_user["id"],
            asset=request.asset,
            amount=request.amount,
            apr=apr,
            since=datetime.utcnow(),
            until=datetime.utcnow() + timedelta(days=request.duration_days),
            is_active=True
        )
        
        # Lock funds
        balance.amount -= request.amount
        balance.available = balance.amount - balance.reserved
        await db.commit()
        
        db.add(stake)
        await db.commit()
        await db.refresh(stake)
        
        return StakeResponse(
            id=stake.id,
            user_id=stake.user_id,
            asset=stake.asset,
            amount=stake.amount,
            apr=stake.apr,
            since=stake.since,
            until=stake.until,
            is_active=stake.is_active,
            rewards_claimed=stake.rewards_claimed,
            created_at=stake.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create stake"
        )

@router.post("/unstake")
async def unstake(
    request: UnstakeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Unstake tokens"""
    try:
        # Get stake
        result = await db.execute(
            select(Stake).where(
                Stake.id == request.stake_id,
                Stake.user_id == current_user["id"]
            )
        )
        stake = result.scalar_one_or_none()
        
        if not stake:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stake not found"
            )
        
        if not stake.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stake not active"
            )
        
        # Deactivate stake
        stake.is_active = False
        
        # Return funds
        from routers.wallet import update_balance
        await update_balance(db, current_user["id"], stake.asset, stake.amount)
        
        await db.commit()
        
        return {"success": True, "amount": stake.amount, "asset": stake.asset}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unstake"
        )

@router.post("/claim_rewards")
async def claim_rewards(
    request: ClaimRewardsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Claim staking rewards"""
    try:
        # Get stake
        result = await db.execute(
            select(Stake).where(
                Stake.id == request.stake_id,
                Stake.user_id == current_user["id"]
            )
        )
        stake = result.scalar_one_or_none()
        
        if not stake:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stake not found"
            )
        
        # Calculate rewards
        days_staked = (datetime.utcnow() - stake.since).days
        total_rewards = stake.amount * stake.apr / Decimal("365") * days_staked
        unclaimed_rewards = total_rewards - stake.rewards_claimed
        
        if unclaimed_rewards <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No rewards to claim"
            )
        
        # Update stake
        stake.rewards_claimed = total_rewards
        
        # Credit rewards
        from routers.wallet import update_balance
        await update_balance(db, current_user["id"], stake.asset, unclaimed_rewards)
        
        await db.commit()
        
        return {"success": True, "rewards": unclaimed_rewards, "asset": stake.asset}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to claim rewards"
        )
