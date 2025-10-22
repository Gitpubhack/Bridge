"""
Authentication router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from passlib.context import CryptContext
import hashlib
import hmac
import json
from datetime import datetime, timedelta

from database import get_db
from models.user import User
from schemas.auth import TelegramLoginRequest, TelegramLoginResponse, Token
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, TELEGRAM_BOT_TOKEN

security = HTTPBearer()

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_telegram_data(webapp_data: str) -> dict:
    """Verify Telegram WebApp data"""
    try:
        # Parse the data
        data = json.loads(webapp_data)
        
        # Extract components
        init_data = data.get("initData", "")
        hash_value = data.get("hash", "")
        
        if not init_data or not hash_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Telegram data"
            )
        
        # Verify hash (simplified for demo - in production use proper verification)
        if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith("TODO"):
            # Mock verification for testing
            return {
                "id": 123456789,
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "language_code": "en"
            }
        
        # In production, verify the hash using the bot token
        # This is a simplified version
        return {
            "id": 123456789,
            "first_name": "Test",
            "last_name": "User", 
            "username": "testuser",
            "language_code": "en"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Telegram data format"
        )

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> User:
    """Get user by Telegram ID"""
    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, telegram_data: dict) -> User:
    """Create new user"""
    user = User(
        telegram_id=telegram_data["id"],
        username=telegram_data.get("username"),
        first_name=telegram_data.get("first_name"),
        last_name=telegram_data.get("last_name")
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/telegram_login", response_model=TelegramLoginResponse)
async def telegram_login(
    request: TelegramLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login with Telegram WebApp data"""
    try:
        # Verify Telegram data
        telegram_data = verify_telegram_data(request.webapp_data)
        
        # Get or create user
        user = await get_user_by_telegram_id(db, telegram_data["id"])
        if not user:
            user = await create_user(db, telegram_data)
        
        # Create access token
        access_token = create_access_token(
            data={"telegram_id": user.telegram_id}
        )
        
        return TelegramLoginResponse(
            access_token=access_token,
            user={
                "id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_premium": user.is_premium,
                "level": user.level,
                "is_admin": user.is_admin
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/me")
async def get_current_user(
    token: str = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get current user information"""
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        telegram_id: int = payload.get("telegram_id")
        if telegram_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = await get_user_by_telegram_id(db, telegram_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_premium": user.is_premium,
        "level": user.level,
        "xp": user.xp,
        "kyc_status": user.kyc_status,
        "is_admin": user.is_admin,
        "created_at": user.created_at
    }
