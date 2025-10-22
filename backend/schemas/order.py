"""
Order and Trade schemas
"""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from models.order import OrderSide, OrderType, OrderStatus

class OrderCreate(BaseModel):
    user_id: int
    pair: str
    side: OrderSide
    type: OrderType
    price: Optional[Decimal] = None
    amount: Decimal
    immediate_fill: bool = False

class OrderResponse(BaseModel):
    id: int
    user_id: int
    pair: str
    side: OrderSide
    type: OrderType
    price: Optional[Decimal]
    amount: Decimal
    filled: Decimal
    remaining: Decimal
    status: OrderStatus
    fee: Decimal
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class OrderBookEntry(BaseModel):
    price: Decimal
    amount: Decimal
    total: Decimal

class OrderBookResponse(BaseModel):
    pair: str
    bids: list[OrderBookEntry]
    asks: list[OrderBookEntry]
    timestamp: datetime

class TradeResponse(BaseModel):
    id: int
    buy_order_id: int
    sell_order_id: int
    pair: str
    price: Decimal
    amount: Decimal
    fee: Decimal
    buyer_id: int
    seller_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CancelOrderRequest(BaseModel):
    user_id: int
    order_id: int
