"""
Exchange router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from decimal import Decimal
from typing import List, Dict, Any, Optional
from datetime import datetime

from database import get_db
from models.user import User
from models.balance import Balance
from models.order import Order, OrderBook, Trade, OrderSide, OrderType, OrderStatus
from models.transaction import Transaction, TransactionType, TransactionStatus
from schemas.order import (
    OrderCreate, OrderResponse, OrderBookResponse, OrderBookEntry,
    TradeResponse, CancelOrderRequest
)
from services.bybit import BybitClient
from routers.auth import get_current_user

router = APIRouter()
bybit = BybitClient()

async def get_order_book_entries(
    db: AsyncSession, 
    pair: str, 
    side: OrderSide, 
    limit: int = 25
) -> List[OrderBookEntry]:
    """Get order book entries for a pair and side"""
    result = await db.execute(
        select(OrderBook)
        .where(and_(OrderBook.pair == pair, OrderBook.side == side))
        .order_by(OrderBook.price.desc() if side == OrderSide.BUY else OrderBook.price.asc())
        .limit(limit)
    )
    
    entries = result.scalars().all()
    return [
        OrderBookEntry(
            price=entry.price,
            amount=entry.amount,
            total=entry.price * entry.amount
        )
        for entry in entries
    ]

async def match_orders(db: AsyncSession, new_order: Order) -> List[Trade]:
    """Simple matching engine"""
    trades = []
    
    # Get opposite side orders
    opposite_side = OrderSide.SELL if new_order.side == OrderSide.BUY else OrderSide.BUY
    
    result = await db.execute(
        select(Order)
        .where(and_(
            Order.pair == new_order.pair,
            Order.side == opposite_side,
            Order.status == OrderStatus.PENDING,
            Order.remaining > 0
        ))
        .order_by(Order.price.asc() if opposite_side == OrderSide.SELL else Order.price.desc())
    )
    
    opposite_orders = result.scalars().all()
    
    remaining_amount = new_order.remaining
    
    for opposite_order in opposite_orders:
        if remaining_amount <= 0:
            break
            
        # Check if orders can match
        if new_order.side == OrderSide.BUY:
            if new_order.price < opposite_order.price:
                break
        else:
            if new_order.price > opposite_order.price:
                break
        
        # Calculate trade amount
        trade_amount = min(remaining_amount, opposite_order.remaining)
        trade_price = opposite_order.price  # Use existing order price
        
        # Create trade
        trade = Trade(
            buy_order_id=new_order.id if new_order.side == OrderSide.BUY else opposite_order.id,
            sell_order_id=opposite_order.id if new_order.side == OrderSide.BUY else new_order.id,
            pair=new_order.pair,
            price=trade_price,
            amount=trade_amount,
            fee=trade_amount * Decimal("0.001"),  # 0.1% fee
            buyer_id=new_order.user_id if new_order.side == OrderSide.BUY else opposite_order.user_id,
            seller_id=opposite_order.user_id if new_order.side == OrderSide.BUY else new_order.user_id
        )
        
        db.add(trade)
        trades.append(trade)
        
        # Update order amounts
        new_order.filled += trade_amount
        new_order.remaining -= trade_amount
        opposite_order.filled += trade_amount
        opposite_order.remaining -= trade_amount
        
        # Update order statuses
        if new_order.remaining <= 0:
            new_order.status = OrderStatus.FILLED
        elif new_order.filled > 0:
            new_order.status = OrderStatus.PARTIALLY_FILLED
            
        if opposite_order.remaining <= 0:
            opposite_order.status = OrderStatus.FILLED
        elif opposite_order.filled > 0:
            opposite_order.status = OrderStatus.PARTIALLY_FILLED
        
        remaining_amount -= trade_amount
        
        # Update balances
        await update_balances_for_trade(db, trade)
    
    return trades

async def update_balances_for_trade(db: AsyncSession, trade: Trade):
    """Update user balances after a trade"""
    # Get base and quote assets from pair
    base_asset, quote_asset = trade.pair.split("/")
    
    # Update buyer balance (receive base, pay quote)
    buyer_quote_balance = await get_user_balance(db, trade.buyer_id, quote_asset)
    buyer_quote_balance.amount -= trade.price * trade.amount
    buyer_quote_balance.available = buyer_quote_balance.amount - buyer_quote_balance.reserved
    
    buyer_base_balance = await get_user_balance(db, trade.buyer_id, base_asset)
    buyer_base_balance.amount += trade.amount
    buyer_base_balance.available = buyer_base_balance.amount - buyer_base_balance.reserved
    
    # Update seller balance (receive quote, pay base)
    seller_base_balance = await get_user_balance(db, trade.seller_id, base_asset)
    seller_base_balance.amount -= trade.amount
    seller_base_balance.available = seller_base_balance.amount - seller_base_balance.reserved
    
    seller_quote_balance = await get_user_balance(db, trade.seller_id, quote_asset)
    seller_quote_balance.amount += trade.price * trade.amount
    seller_quote_balance.available = seller_quote_balance.amount - seller_quote_balance.reserved

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

@router.post("/order")
async def place_order(
    request: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Place a trading order"""
    try:
        # Validate order
        if request.type == OrderType.LIMIT and not request.price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Price required for limit orders"
            )
        
        # Get base and quote assets
        base_asset, quote_asset = request.pair.split("/")
        
        # Check balance for the order
        if request.side == OrderSide.BUY:
            # Need quote currency
            balance = await get_user_balance(db, current_user["id"], quote_asset)
            required_amount = request.amount * (request.price or Decimal("0"))
            
            if balance.available < required_amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance"
                )
        else:
            # Need base currency
            balance = await get_user_balance(db, current_user["id"], base_asset)
            if balance.available < request.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance"
                )
        
        # Create order
        order = Order(
            user_id=current_user["id"],
            pair=request.pair,
            side=request.side,
            type=request.type,
            price=request.price,
            amount=request.amount,
            remaining=request.amount,
            status=OrderStatus.PENDING
        )
        
        db.add(order)
        await db.commit()
        await db.refresh(order)
        
        # Reserve funds
        if request.side == OrderSide.BUY:
            balance.reserved += required_amount
        else:
            balance.reserved += request.amount
        
        balance.available = balance.amount - balance.reserved
        await db.commit()
        
        # Add to order book
        order_book_entry = OrderBook(
            pair=request.pair,
            side=request.side,
            price=request.price or Decimal("0"),
            amount=request.amount,
            order_id=order.id
        )
        db.add(order_book_entry)
        await db.commit()
        
        # Try to match orders
        trades = await match_orders(db, order)
        
        # If immediate fill requested and no matches, try external liquidity
        if request.immediate_fill and not trades:
            await try_external_liquidity(db, order)
        
        return {
            "order_id": order.id,
            "status": order.status.value,
            "filled": order.filled,
            "remaining": order.remaining,
            "trades": len(trades)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to place order"
        )

async def try_external_liquidity(db: AsyncSession, order: Order):
    """Try to fill order using external liquidity (Bybit)"""
    try:
        # Get market data from Bybit
        ticker = await bybit.get_ticker(order.pair)
        
        if ticker.get("retCode") == 0:
            # Place market order on Bybit (simplified)
            bybit_order = await bybit.place_order(
                symbol=order.pair,
                side=order.side.value,
                order_type="Market",
                qty=str(order.amount)
            )
            
            if bybit_order.get("retCode") == 0:
                # Update order as filled
                order.status = OrderStatus.FILLED
                order.filled = order.amount
                order.remaining = Decimal("0")
                await db.commit()
                
                # Create trade record
                trade = Trade(
                    buy_order_id=order.id if order.side == OrderSide.BUY else 0,
                    sell_order_id=0 if order.side == OrderSide.BUY else order.id,
                    pair=order.pair,
                    price=Decimal(ticker["result"]["list"][0]["lastPrice"]),
                    amount=order.amount,
                    fee=order.amount * Decimal("0.001"),
                    buyer_id=order.user_id if order.side == OrderSide.BUY else 0,
                    seller_id=0 if order.side == OrderSide.BUY else order.user_id
                )
                db.add(trade)
                await db.commit()
                
    except Exception as e:
        # External liquidity failed, keep order open
        pass

@router.post("/cancel")
async def cancel_order(
    request: CancelOrderRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cancel an order"""
    try:
        # Get order
        result = await db.execute(
            select(Order).where(
                Order.id == request.order_id,
                Order.user_id == current_user["id"]
            )
        )
        order = result.scalar_one_or_none()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        if order.status not in [OrderStatus.PENDING, OrderStatus.PARTIALLY_FILLED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel order"
            )
        
        # Release reserved funds
        base_asset, quote_asset = order.pair.split("/")
        
        if order.side == OrderSide.BUY:
            balance = await get_user_balance(db, current_user["id"], quote_asset)
            balance.reserved -= order.remaining * (order.price or Decimal("0"))
        else:
            balance = await get_user_balance(db, current_user["id"], base_asset)
            balance.reserved -= order.remaining
        
        balance.available = balance.amount - balance.reserved
        
        # Update order status
        order.status = OrderStatus.CANCELLED
        order.remaining = Decimal("0")
        
        # Remove from order book
        await db.execute(
            select(OrderBook).where(OrderBook.order_id == order.id)
        )
        
        await db.commit()
        
        return {"success": True, "order_id": order.id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel order"
        )

@router.get("/orderbook")
async def get_orderbook(
    pair: str,
    limit: int = 25,
    db: AsyncSession = Depends(get_db)
):
    """Get order book for a trading pair"""
    try:
        bids = await get_order_book_entries(db, pair, OrderSide.BUY, limit)
        asks = await get_order_book_entries(db, pair, OrderSide.SELL, limit)
        
        return OrderBookResponse(
            pair=pair,
            bids=bids,
            asks=asks,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get order book"
        )

@router.get("/trades")
async def get_trades(
    user_id: int,
    pair: Optional[str] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user trade history"""
    # Check if user is requesting their own trades or is admin
    if current_user["id"] != user_id and not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        query = select(Trade).where(
            or_(Trade.buyer_id == user_id, Trade.seller_id == user_id)
        )
        
        if pair:
            query = query.where(Trade.pair == pair)
        
        query = query.order_by(Trade.created_at.desc()).limit(limit)
        
        result = await db.execute(query)
        trades = result.scalars().all()
        
        return [
            TradeResponse(
                id=trade.id,
                buy_order_id=trade.buy_order_id,
                sell_order_id=trade.sell_order_id,
                pair=trade.pair,
                price=trade.price,
                amount=trade.amount,
                fee=trade.fee,
                buyer_id=trade.buyer_id,
                seller_id=trade.seller_id,
                created_at=trade.created_at
            )
            for trade in trades
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get trades"
        )
