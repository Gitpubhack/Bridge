"""
Bridge Exchange - FastAPI Application without Database
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Security
security = HTTPBearer()

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
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2023-01-01T00:00:00Z"
    }

@app.get("/api/auth/telegram_login")
async def telegram_login():
    """Mock Telegram login endpoint"""
    return {
        "access_token": "mock_token_123",
        "user": {
            "id": 1,
            "telegram_id": 123456789,
            "username": "test_user",
            "is_premium": False,
            "level": 1
        }
    }

@app.get("/api/wallet/balances/{user_id}")
async def get_balances(user_id: int):
    """Mock balances endpoint"""
    return {
        "user_id": user_id,
        "balances": {
            "USDT": "1000.00",
            "BTC": "0.05",
            "ETH": "2.5"
        }
    }

@app.post("/api/wallet/deposit")
async def deposit():
    """Mock deposit endpoint"""
    return {
        "invoice_id": "inv_123",
        "pay_url": "https://pay.crypt.bot/pay/inv_123",
        "status": "pending"
    }

@app.post("/api/wallet/withdraw")
async def withdraw():
    """Mock withdraw endpoint"""
    return {
        "withdraw_id": "wdr_123",
        "status": "pending"
    }

@app.get("/api/exchange/orderbook")
async def get_orderbook(pair: str = "BTC/USDT"):
    """Mock orderbook endpoint"""
    return {
        "pair": pair,
        "bids": [
            {"price": "50000.00", "amount": "0.1"},
            {"price": "49999.00", "amount": "0.2"}
        ],
        "asks": [
            {"price": "50001.00", "amount": "0.1"},
            {"price": "50002.00", "amount": "0.2"}
        ]
    }

@app.post("/api/exchange/order")
async def place_order():
    """Mock place order endpoint"""
    return {
        "order_id": "ord_123",
        "status": "pending"
    }

@app.get("/api/nft/listings")
async def get_nft_listings():
    """Mock NFT listings endpoint"""
    return {
        "listings": [
            {
                "id": 1,
                "name": "Cool NFT #1",
                "price": "100.00",
                "owner": "user123"
            }
        ]
    }

@app.post("/api/nft/mint")
async def mint_nft():
    """Mock NFT mint endpoint"""
    return {
        "nft_id": "nft_123",
        "token_id": "token_456",
        "status": "minted"
    }

@app.get("/api/ai/portfolio/{user_id}")
async def get_portfolio_advice(user_id: int):
    """Mock AI portfolio advice endpoint"""
    return {
        "user_id": user_id,
        "risk_level": "medium",
        "suggestions": [
            "Consider diversifying your portfolio",
            "BTC shows strong potential",
            "Monitor market volatility"
        ],
        "allocation": {
            "BTC": "40%",
            "ETH": "30%",
            "USDT": "30%"
        }
    }

@app.post("/api/ai/chat")
async def chat_with_ai():
    """Mock AI chat endpoint"""
    return {
        "response": "Hello! I'm your AI trading assistant. How can I help you today?",
        "suggestions": [
            "Check your portfolio balance",
            "View market trends",
            "Get trading advice"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_no_db:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
