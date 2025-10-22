"""
Bridge Exchange - Working FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Абсолютный путь к папке frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Монтируем папку assets как /assets
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

# Отдаём index.html при открытии сайта
@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
    
# Пути к фронтенду
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Подключаем статические файлы (CSS, JS, изображения и т.д.)
#app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

# Главная страница (index.html)
@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="../frontend/assets"), name="static")

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

import os
from fastapi.responses import FileResponse

@app.get("/frontend")
async def frontend():
    """Serve frontend"""
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(os.path.abspath(frontend_path))

# Authentication endpoints
@app.post("/api/auth/telegram_login")
async def telegram_login(data: Dict[str, Any]):
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
async def deposit(data: Dict[str, Any]):
    """Create deposit invoice"""
    return {
        "invoice_id": "inv_123456",
        "pay_url": "https://pay.crypt.bot/pay/inv_123456",
        "status": "pending",
        "amount": data.get("amount", "100.00"),
        "asset": data.get("asset", "USDT")
    }

@app.post("/api/wallet/withdraw")
async def withdraw(data: Dict[str, Any]):
    """Create withdraw request"""
    return {
        "withdraw_id": "wdr_123456",
        "status": "pending",
        "amount": data.get("amount", "50.00"),
        "asset": data.get("asset", "USDT"),
        "to_address": data.get("to_address", "0x123...")
    }

@app.post("/api/wallet/transfer")
async def transfer(data: Dict[str, Any]):
    """Internal transfer"""
    return {
        "transfer_id": "trf_123456",
        "status": "completed",
        "amount": data.get("amount", "10.00"),
        "asset": data.get("asset", "USDT"),
        "to_user": data.get("to_user", 2)
    }

# Exchange endpoints
@app.get("/api/exchange/orderbook")
async def get_orderbook(pair: str = "BTC/USDT"):
    """Get orderbook"""
    return {
        "pair": pair,
        "bids": [
            {"price": "50000.00", "amount": "0.1", "total": "5000.00"},
            {"price": "49999.00", "amount": "0.2", "total": "9999.80"},
            {"price": "49998.00", "amount": "0.15", "total": "7499.70"}
        ],
        "asks": [
            {"price": "50001.00", "amount": "0.1", "total": "5000.10"},
            {"price": "50002.00", "amount": "0.2", "total": "10000.40"},
            {"price": "50003.00", "amount": "0.15", "total": "7500.45"}
        ],
        "last_price": "50000.50",
        "volume_24h": "1250000.00"
    }

@app.post("/api/exchange/order")
async def place_order(data: Dict[str, Any]):
    """Place order"""
    return {
        "order_id": "ord_123456",
        "status": "pending",
        "pair": data.get("pair", "BTC/USDT"),
        "side": data.get("side", "buy"),
        "type": data.get("type", "limit"),
        "price": data.get("price", "50000.00"),
        "amount": data.get("amount", "0.1")
    }

@app.post("/api/exchange/cancel")
async def cancel_order(data: Dict[str, Any]):
    """Cancel order"""
    return {
        "order_id": data.get("order_id", "ord_123456"),
        "status": "cancelled"
    }

@app.get("/api/exchange/trades")
async def get_trades(user_id: int = 1, pair: str = "BTC/USDT"):
    """Get user trades"""
    return {
        "trades": [
            {
                "id": "trd_001",
                "pair": pair,
                "side": "buy",
                "price": "50000.00",
                "amount": "0.1",
                "fee": "5.00",
                "timestamp": "2023-01-01T12:00:00Z"
            }
        ]
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
                "image_url": "https://example.com/nft1.jpg",
                "token_id": "token_001"
            },
            {
                "id": 2,
                "name": "Awesome NFT #2",
                "description": "An awesome NFT",
                "price": "200.00",
                "owner": "user456",
                "image_url": "https://example.com/nft2.jpg",
                "token_id": "token_002"
            }
        ]
    }

@app.post("/api/nft/mint")
async def mint_nft(data: Dict[str, Any]):
    """Mint NFT"""
    return {
        "nft_id": "nft_123456",
        "token_id": "token_789",
        "status": "minted",
        "metadata": data.get("metadata", {}),
        "owner": data.get("owner", "user123")
    }

@app.post("/api/nft/buy")
async def buy_nft(data: Dict[str, Any]):
    """Buy NFT"""
    return {
        "purchase_id": "pur_123456",
        "status": "completed",
        "nft_id": data.get("nft_id", "nft_123456"),
        "price": data.get("price", "100.00"),
        "buyer": data.get("buyer", "user123")
    }

# P2P endpoints
@app.get("/api/p2p/offers")
async def get_p2p_offers():
    """Get P2P offers"""
    return {
        "offers": [
            {
                "id": 1,
                "seller": "user123",
                "amount": "1000.00",
                "asset": "USDT",
                "price": "1.00",
                "payment_method": "Bank Transfer",
                "status": "active"
            }
        ]
    }

@app.post("/api/p2p/offer")
async def create_p2p_offer(data: Dict[str, Any]):
    """Create P2P offer"""
    return {
        "offer_id": "p2p_123456",
        "status": "active",
        "amount": data.get("amount", "1000.00"),
        "asset": data.get("asset", "USDT"),
        "price": data.get("price", "1.00")
    }

# Staking endpoints
@app.get("/api/stake/pools")
async def get_staking_pools():
    """Get staking pools"""
    return {
        "pools": [
            {
                "id": 1,
                "asset": "USDT",
                "apr": "12.5",
                "min_amount": "100.00",
                "lock_period": "30 days"
            }
        ]
    }

@app.post("/api/stake")
async def stake(data: Dict[str, Any]):
    """Stake tokens"""
    return {
        "stake_id": "stake_123456",
        "status": "active",
        "amount": data.get("amount", "1000.00"),
        "asset": data.get("asset", "USDT"),
        "apr": "12.5"
    }

# DAO endpoints
@app.get("/api/dao/proposals")
async def get_dao_proposals():
    """Get DAO proposals"""
    return {
        "proposals": [
            {
                "id": 1,
                "title": "Increase USDT staking APR",
                "description": "Proposal to increase USDT staking APR from 12% to 15%",
                "status": "active",
                "votes_for": 150,
                "votes_against": 25,
                "created_by": "user123"
            }
        ]
    }

@app.post("/api/dao/vote")
async def vote_proposal(data: Dict[str, Any]):
    """Vote on proposal"""
    return {
        "vote_id": "vote_123456",
        "status": "recorded",
        "proposal_id": data.get("proposal_id", 1),
        "vote": data.get("vote", "for")
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
        },
        "recommended_actions": [
            "Buy more ETH if price drops below $3000",
            "Consider staking USDT for 12.5% APR",
            "Set stop-loss at 5% for BTC position"
        ]
    }

@app.post("/api/ai/chat")
async def chat_with_ai(data: Dict[str, Any]):
    """Chat with AI assistant"""
    message = data.get("message", "Hello")
    return {
        "response": f"AI Assistant: I understand you said '{message}'. How can I help you with your trading today?",
        "suggestions": [
            "Check your portfolio balance",
            "View market trends",
            "Get trading advice",
            "Learn about DeFi strategies"
        ]
    }

# Support endpoints
@app.get("/api/support/tickets")
async def get_support_tickets(user_id: int = 1):
    """Get support tickets"""
    return {
        "tickets": [
            {
                "id": 1,
                "subject": "Withdrawal issue",
                "status": "open",
                "created_at": "2023-01-01T10:00:00Z",
                "last_message": "Please help with my withdrawal"
            }
        ]
    }

@app.post("/api/support/ticket")
async def create_support_ticket(data: Dict[str, Any]):
    """Create support ticket"""
    return {
        "ticket_id": "tkt_123456",
        "status": "open",
        "subject": data.get("subject", "Support request"),
        "created_at": "2023-01-01T10:00:00Z"
    }

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram webhook"""
    data = await request.json()
    print("📩 Incoming Telegram webhook:", data)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run(
        "main_working:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
