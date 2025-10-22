"""
Admin router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from decimal import Decimal
from typing import Dict, Any

from database import get_db
from models.user import User
from models.transaction import Transaction
from models.balance import Balance
from models.ticket import Ticket
from schemas.admin import (
    AdminActionRequest, AdjustBalanceRequest, FreezeUserRequest, 
    RefundRequest, AdminLogResponse, AdminStatsResponse
)
from routers.auth import get_current_user

router = APIRouter()

async def check_admin_permissions(current_user: dict):
    """Check if user has admin permissions"""
    if not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

@router.get("/stats")
async def get_admin_stats(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get admin dashboard statistics"""
    await check_admin_permissions(current_user)
    
    try:
        # Get user counts
        user_result = await db.execute(select(func.count(User.id)))
        total_users = user_result.scalar()
        
        active_user_result = await db.execute(
            select(func.count(User.id)).where(User.is_active == True)
        )
        active_users = active_user_result.scalar()
        
        # Get transaction volume (simplified)
        volume_result = await db.execute(
            select(func.sum(Transaction.amount)).where(
                Transaction.status == "completed",
                Transaction.asset == "USDT"
            )
        )
        total_volume = volume_result.scalar() or Decimal("0")
        
        # Get pending withdrawals
        pending_result = await db.execute(
            select(func.count(Transaction.id)).where(
                Transaction.type == "withdraw",
                Transaction.status == "pending"
            )
        )
        pending_withdrawals = pending_result.scalar()
        
        # Get open tickets
        ticket_result = await db.execute(
            select(func.count(Ticket.id)).where(Ticket.status == "open")
        )
        open_tickets = ticket_result.scalar()
        
        # Get total balances
        balance_result = await db.execute(
            select(Balance.asset, func.sum(Balance.amount))
            .group_by(Balance.asset)
        )
        total_balances = {row[0]: row[1] for row in balance_result.fetchall()}
        
        return AdminStatsResponse(
            total_users=total_users,
            active_users=active_users,
            total_volume_24h=total_volume,
            pending_withdrawals=pending_withdrawals,
            open_tickets=open_tickets,
            total_balance=total_balances
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get stats"
        )

@router.post("/adjust_balance")
async def adjust_user_balance(
    request: AdjustBalanceRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Adjust user balance (admin only)"""
    await check_admin_permissions(current_user)
    
    try:
        # Get user
        result = await db.execute(
            select(User).where(User.id == request.user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get or create balance
        from routers.wallet import get_user_balance
        balance = await get_user_balance(db, request.user_id, request.asset)
        
        # Adjust balance
        balance.amount += request.amount
        balance.available = balance.amount - balance.reserved
        await db.commit()
        
        # Create transaction record
        from models.transaction import Transaction, TransactionType, TransactionStatus
        transaction = Transaction(
            user_id=request.user_id,
            type=TransactionType.REWARD,  # Admin adjustment
            amount=request.amount,
            asset=request.asset,
            status=TransactionStatus.COMPLETED,
            meta={"admin_action": "balance_adjustment", "reason": request.reason}
        )
        db.add(transaction)
        await db.commit()
        
        return {"success": True, "new_balance": balance.amount}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to adjust balance"
        )

@router.post("/freeze_user")
async def freeze_user(
    request: FreezeUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Freeze user account"""
    await check_admin_permissions(current_user)
    
    try:
        # Get user
        result = await db.execute(
            select(User).where(User.id == request.user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Freeze user
        user.is_active = False
        await db.commit()
        
        return {"success": True, "user_id": request.user_id, "frozen": True}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to freeze user"
        )

@router.post("/refund")
async def process_refund(
    request: RefundRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Process refund for transaction"""
    await check_admin_permissions(current_user)
    
    try:
        # Get transaction
        result = await db.execute(
            select(Transaction).where(Transaction.id == request.transaction_id)
        )
        transaction = result.scalar_one_or_none()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Process refund
        refund_amount = request.amount or transaction.amount
        
        from routers.wallet import update_balance
        await update_balance(db, transaction.user_id, transaction.asset, refund_amount)
        
        # Create refund transaction
        refund_transaction = Transaction(
            user_id=transaction.user_id,
            type=TransactionType.REFUND,
            amount=refund_amount,
            asset=transaction.asset,
            status=TransactionStatus.COMPLETED,
            meta={"original_transaction_id": transaction.id, "reason": request.reason}
        )
        db.add(refund_transaction)
        await db.commit()
        
        return {"success": True, "refund_amount": refund_amount}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process refund"
        )
