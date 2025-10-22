"""
AI Assistant router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any

from database import get_db
from models.balance import Balance
from models.transaction import Transaction
from services.openai_assistant import OpenAIAssistant
from services.gecko import GeckoClient
from routers.auth import get_current_user

router = APIRouter()
ai_assistant = OpenAIAssistant()
gecko_client = GeckoClient()

@router.post("/portfolio")
async def analyze_portfolio(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Analyze user portfolio with AI"""
    # Check if user is requesting their own analysis or is admin
    if current_user["id"] != user_id and not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        # Get user balances
        result = await db.execute(
            select(Balance).where(Balance.user_id == user_id)
        )
        balances = result.scalars().all()
        
        user_balances = {balance.asset: float(balance.amount) for balance in balances}
        
        # Get recent trades
        trade_result = await db.execute(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
            .limit(50)
        )
        trades = trade_result.scalars().all()
        
        trade_history = [
            {
                "type": trade.type.value,
                "amount": float(trade.amount),
                "asset": trade.asset,
                "created_at": trade.created_at.isoformat()
            }
            for trade in trades
        ]
        
        # Get market data
        market_data = await gecko_client.get_price(
            ids=["bitcoin", "ethereum", "tether"],
            vs_currencies=["usd"]
        )
        
        # Analyze portfolio
        analysis = await ai_assistant.analyze_portfolio(
            user_balances=user_balances,
            trade_history=trade_history,
            market_data=market_data
        )
        
        return analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze portfolio"
        )

@router.post("/chat")
async def chat_with_ai(
    message: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Chat with AI assistant"""
    try:
        # Get user context
        context = {
            "user_id": current_user["id"],
            "username": current_user.get("username"),
            "level": current_user.get("level", 1)
        }
        
        # Get AI response
        response = await ai_assistant.chat_assistant(message, context)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get AI response"
        )

@router.post("/trading_signal")
async def get_trading_signal(
    pair: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get AI trading signal for a pair"""
    try:
        # Get market data
        market_data = await gecko_client.get_price(
            ids=[pair.split("/")[0].lower()],
            vs_currencies=["usd"]
        )
        
        # Generate signal
        signal = await ai_assistant.generate_trading_signal(pair, market_data)
        
        return signal
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate trading signal"
        )
