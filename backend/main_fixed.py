"""
Bridge Exchange - Fixed FastAPI Main Application
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import with proper paths
from config import ALLOWED_ORIGINS, DEBUG
from database import init_db
from routers import (
    auth, wallet, exchange, nft, p2p, stake, dao, 
    admin, support, ai
)

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

# Create FastAPI app
app = FastAPI(
    title="Bridge Exchange API",
    description="Hybrid crypto exchange with Telegram Mini App integration",
    version="1.0.0",
    debug=DEBUG,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(wallet.router, prefix="/api/wallet", tags=["Wallet"])
app.include_router(exchange.router, prefix="/api/exchange", tags=["Exchange"])
app.include_router(nft.router, prefix="/api/nft", tags=["NFT"])
app.include_router(p2p.router, prefix="/api/p2p", tags=["P2P"])
app.include_router(stake.router, prefix="/api/stake", tags=["Staking"])
app.include_router(dao.router, prefix="/api/dao", tags=["DAO"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(support.router, prefix="/api/support", tags=["Support"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Assistant"])

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

if __name__ == "__main__":
    uvicorn.run(
        "main_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )



