"""
Bridge Exchange - Simple Fixed FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
import sys
from typing import Dict, Any

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Create FastAPI app
app = FastAPI(
    title="Bridge Exchange API",
    description="Hybrid crypto exchange with Telegram Mini App integration",
    version="1.0.0",
    debug=True
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Bridge Exchange API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "frontend": "/frontend"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2023-01-01T00:00:00Z"
    }

@app.get("/frontend")
async def frontend():
    """Serve frontend"""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {"message": "Frontend not found", "path": frontend_path}

# Authentication endpoints
@app.post("/api/auth/telegram_login")
async def telegram_login(data: Dict[str, Any] = None):
    """Telegram login endpoint"""
    return {
        "access_token": "mock_token_123456",
        "user": {
            "id": 1,
            "telegram_id": 123456789,
            "username": "test_user",
            "first_name": "Test",
            "last_name": "User",
            "is_premium": False,
            "level": 1,
            "xp": 100,
            "kyc_status": "pending"
        }
    }

# Wallet endpoints
@app.get("/api/wallet/balances/{user_id}")
async def get_balances(user_id: int):
    """Get user balances"""
    return {
        "user_id": user_id,
        "balances": {
            "USDT": {"amount": "1000.00", "reserved": "0.00"},
            "BTC": {"amount": "0.05", "reserved": "0.00"},
            "ETH": {"amount": "2.5", "reserved": "0.00"},
            "TON": {"amount": "100.00", "reserved": "0.00"}
        }
    }

@app.post("/api/wallet/deposit")
async def deposit(data: Dict[str, Any] = None):
    """Create deposit invoice"""
    return {
        "invoice_id": "inv_123456",
        "pay_url": "https://pay.crypt.bot/pay/inv_123456",
        "status": "pending",
        "amount": "100.00",
        "asset": "USDT"
    }

@app.post("/api/wallet/withdraw")
async def withdraw(data: Dict[str, Any] = None):
    """Create withdraw request"""
    return {
        "withdraw_id": "wdr_123456",
        "status": "pending",
        "amount": "50.00",
        "asset": "USDT",
        "to_address": "0x123..."
    }

# Exchange endpoints
@app.get("/api/exchange/orderbook")
async def get_orderbook(pair: str = "BTC/USDT"):
    """Get orderbook"""
    return {
        "pair": pair,
        "bids": [
            {"price": "50000.00", "amount": "0.1", "total": "5000.00"},
            {"price": "49999.00", "amount": "0.2", "total": "9999.80"}
        ],
        "asks": [
            {"price": "50001.00", "amount": "0.1", "total": "5000.10"},
            {"price": "50002.00", "amount": "0.2", "total": "10000.40"}
        ],
        "last_price": "50000.50",
        "volume_24h": "1250000.00"
    }

@app.post("/api/exchange/order")
async def place_order(data: Dict[str, Any] = None):
    """Place order"""
    return {
        "order_id": "ord_123456",
        "status": "pending",
        "pair": "BTC/USDT",
        "side": "buy",
        "type": "limit",
        "price": "50000.00",
        "amount": "0.1"
    }

# NFT endpoints
@app.get("/api/nft/listings")
async def get_nft_listings():
    """Get NFT listings"""
    return {
        "listings": [
            {
                "id": 1,
                "name": "Cool NFT #1",
                "description": "A very cool NFT",
                "price": "100.00",
                "owner": "user123",
                "image_url": "https://example.com/nft1.jpg"
            }
        ]
    }

@app.post("/api/nft/mint")
async def mint_nft(data: Dict[str, Any] = None):
    """Mint NFT"""
    return {
        "nft_id": "nft_123456",
        "token_id": "token_789",
        "status": "minted",
        "metadata": {},
        "owner": "user123"
    }

# AI endpoints
@app.get("/api/ai/portfolio/{user_id}")
async def get_portfolio_advice(user_id: int):
    """Get AI portfolio advice"""
    return {
        "user_id": user_id,
        "risk_level": "medium",
        "suggestions": [
            "Consider diversifying your portfolio with more ETH",
            "BTC shows strong potential for growth",
            "Monitor market volatility and adjust positions accordingly"
        ],
        "allocation": {
            "BTC": "40%",
            "ETH": "30%",
            "USDT": "30%"
        }
    }

@app.post("/api/ai/chat")
async def chat_with_ai(data: Dict[str, Any] = None):
    """Chat with AI assistant"""
    message = "Hello" if not data else data.get("message", "Hello")
    return {
        "response": f"AI Assistant: I understand you said '{message}'. How can I help you with your trading today?",
        "suggestions": [
            "Check your portfolio balance",
            "View market trends",
            "Get trading advice"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_simple_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
