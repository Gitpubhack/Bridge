"""
Wallet router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal
from typing import List, Dict, Any

from database import get_db
from models.user import User
from models.balance import Balance
from models.transaction import Transaction, TransactionType, TransactionStatus
from models.invoice import Invoice, InvoiceStatus
from schemas.wallet import (
    DepositRequest, WithdrawRequest, TransferRequest, 
    BalanceResponse, WalletResponse
)
from services.cryptopay import CryptoPayClient
from routers.auth import get_current_user

router = APIRouter()
cryptopay = CryptoPayClient()

async def get_user_balance(db: AsyncSession, user_id: int, asset: str) -> Balance:
    """Get user balance for specific asset"""
    result = await db.execute(
        select(Balance).where(
            Balance.user_id == user_id,
            Balance.asset == asset
        )
    )
    balance = result.scalar_one_or_none()
    
    if not balance:
        # Create new balance record
        balance = Balance(
            user_id=user_id,
            asset=asset,
            amount=Decimal("0"),
            reserved=Decimal("0"),
            available=Decimal("0")
        )
        db.add(balance)
        await db.commit()
        await db.refresh(balance)
    
    return balance

async def update_balance(
    db: AsyncSession, 
    user_id: int, 
    asset: str, 
    amount_change: Decimal
) -> Balance:
    """Update user balance"""
    balance = await get_user_balance(db, user_id, asset)
    balance.amount += amount_change
    balance.available = balance.amount - balance.reserved
    await db.commit()
    await db.refresh(balance)
    return balance

@router.post("/deposit")
async def create_deposit(
    request: DepositRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create deposit invoice"""
    try:
        # Create invoice via CryptoPay
        invoice_response = await cryptopay.create_invoice(
            asset=request.asset,
            amount=str(request.amount),
            description=f"Bridge Exchange Deposit - {request.amount} {request.asset}",
            payload=f"user_{current_user['id']}"
        )
        
        if not invoice_response.get("ok"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create invoice"
            )
        
        invoice_data = invoice_response["result"]
        
        # Store invoice in database
        invoice = Invoice(
            user_id=current_user["id"],
            provider_invoice_id=invoice_data["invoice_id"],
            asset=request.asset,
            amount=request.amount,
            status=InvoiceStatus.PENDING,
            pay_url=invoice_data.get("paid_btn_url"),
            raw_data=invoice_data
        )
        
        db.add(invoice)
        await db.commit()
        await db.refresh(invoice)
        
        return {
            "invoice_id": invoice.id,
            "pay_url": invoice.pay_url,
            "amount": request.amount,
            "asset": request.asset,
            "status": "pending"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create deposit"
        )

@router.post("/withdraw")
async def create_withdraw(
    request: WithdrawRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create withdrawal request"""
    try:
        # Check available balance
        balance = await get_user_balance(db, current_user["id"], request.asset)
        if balance.available < request.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )
        
        # Calculate fee (simplified)
        fee = request.amount * Decimal("0.001")  # 0.1% fee
        total_amount = request.amount + fee
        
        if balance.available < total_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance for fee"
            )
        
        # Reserve funds
        balance.reserved += total_amount
        balance.available = balance.amount - balance.reserved
        await db.commit()
        
        # Create transaction
        transaction = Transaction(
            user_id=current_user["id"],
            type=TransactionType.WITHDRAW,
            amount=request.amount,
            asset=request.asset,
            status=TransactionStatus.PENDING,
            fee=fee,
            to_address=request.to_address,
            meta={
                "withdrawal_address": request.to_address,
                "fee": str(fee)
            }
        )
        
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        
        return {
            "transaction_id": transaction.id,
            "amount": request.amount,
            "asset": request.asset,
            "fee": fee,
            "to_address": request.to_address,
            "status": "pending"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create withdrawal"
        )

@router.get("/balances/{user_id}")
async def get_balances(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user balances"""
    # Check if user is requesting their own balances or is admin
    if current_user["id"] != user_id and not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    result = await db.execute(
        select(Balance).where(Balance.user_id == user_id)
    )
    balances = result.scalars().all()
    
    return {
        "user_id": user_id,
        "balances": [
            {
                "asset": balance.asset,
                "amount": balance.amount,
                "reserved": balance.reserved,
                "available": balance.available
            }
            for balance in balances
        ]
    }

@router.post("/transfer")
async def internal_transfer(
    request: TransferRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Internal user-to-user transfer"""
    try:
        # Check if user has sufficient balance
        from_balance = await get_user_balance(db, request.from_user_id, request.asset)
        if from_balance.available < request.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )
        
        # Check if recipient exists
        result = await db.execute(
            select(User).where(User.id == request.to_user_id)
        )
        recipient = result.scalar_one_or_none()
        if not recipient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Recipient not found"
            )
        
        # Perform transfer
        from_balance.amount -= request.amount
        from_balance.available = from_balance.amount - from_balance.reserved
        
        to_balance = await get_user_balance(db, request.to_user_id, request.asset)
        to_balance.amount += request.amount
        to_balance.available = to_balance.amount - to_balance.reserved
        
        # Create transaction records
        from_transaction = Transaction(
            user_id=request.from_user_id,
            type=TransactionType.TRANSFER,
            amount=-request.amount,
            asset=request.asset,
            status=TransactionStatus.COMPLETED,
            to_address=str(request.to_user_id),
            meta={"transfer_to": request.to_user_id}
        )
        
        to_transaction = Transaction(
            user_id=request.to_user_id,
            type=TransactionType.TRANSFER,
            amount=request.amount,
            asset=request.asset,
            status=TransactionStatus.COMPLETED,
            from_address=str(request.from_user_id),
            meta={"transfer_from": request.from_user_id}
        )
        
        db.add(from_transaction)
        db.add(to_transaction)
        await db.commit()
        
        return {
            "success": True,
            "amount": request.amount,
            "asset": request.asset,
            "from_user": request.from_user_id,
            "to_user": request.to_user_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transfer failed"
        )

@router.post("/crypto/webhook")
async def cryptopay_webhook(
    webhook_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """Handle CryptoPay webhook"""
    try:
        # Verify webhook signature (simplified)
        # In production, implement proper signature verification
        
        invoice_id = webhook_data.get("invoice_id")
        status = webhook_data.get("status")
        
        if not invoice_id or status != "paid":
            return {"status": "ignored"}
        
        # Find invoice in database
        result = await db.execute(
            select(Invoice).where(Invoice.provider_invoice_id == invoice_id)
        )
        invoice = result.scalar_one_or_none()
        
        if not invoice:
            return {"status": "invoice_not_found"}
        
        if invoice.status == InvoiceStatus.PAID:
            return {"status": "already_processed"}
        
        # Update invoice status
        invoice.status = InvoiceStatus.PAID
        await db.commit()
        
        # Credit user balance
        await update_balance(db, invoice.user_id, invoice.asset, invoice.amount)
        
        # Create transaction record
        transaction = Transaction(
            user_id=invoice.user_id,
            type=TransactionType.DEPOSIT,
            amount=invoice.amount,
            asset=invoice.asset,
            status=TransactionStatus.COMPLETED,
            meta={"invoice_id": invoice.id}
        )
        
        db.add(transaction)
        await db.commit()
        
        return {"status": "success"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
