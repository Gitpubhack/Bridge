"""
Authentication schemas
"""
from pydantic import BaseModel
from typing import Optional

class TelegramLoginRequest(BaseModel):
    webapp_data: str

class TelegramLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    telegram_id: Optional[int] = None
