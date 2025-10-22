"""
Order and Trade models for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from database import Base
import enum

class OrderSide(enum.Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(enum.Enum):
    LIMIT = "limit"
    MARKET = "market"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    pair = Column(String(20), nullable=False)  # BTC/USDT
    side = Column(Enum(OrderSide), nullable=False)
    type = Column(Enum(OrderType), nullable=False)
    price = Column(Numeric(20, 8), nullable=True)  # Null for market orders
    amount = Column(Numeric(20, 8), nullable=False)
    filled = Column(Numeric(20, 8), default=0)
    remaining = Column(Numeric(20, 8), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    fee = Column(Numeric(20, 8), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, pair={self.pair}, side={self.side}, amount={self.amount})>"

class OrderBook(Base):
    __tablename__ = "order_book"
    
    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(20), nullable=False, index=True)
    side = Column(Enum(OrderSide), nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    order_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<OrderBook(pair={self.pair}, side={self.side}, price={self.price}, amount={self.amount})>"

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    buy_order_id = Column(Integer, nullable=False)
    sell_order_id = Column(Integer, nullable=False)
    pair = Column(String(20), nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    fee = Column(Numeric(20, 8), default=0)
    buyer_id = Column(Integer, nullable=False)
    seller_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Trade(id={self.id}, pair={self.pair}, price={self.price}, amount={self.amount})>"
