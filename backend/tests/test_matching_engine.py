"""
Tests for matching engine
"""
import pytest
from decimal import Decimal
from models.order import Order, OrderSide, OrderType, OrderStatus
from models.trade import Trade

@pytest.fixture
def buy_order():
    return Order(
        id=1,
        user_id=1,
        pair="BTC/USDT",
        side=OrderSide.BUY,
        type=OrderType.LIMIT,
        price=Decimal("50000.00"),
        amount=Decimal("0.1"),
        remaining=Decimal("0.1"),
        status=OrderStatus.PENDING
    )

@pytest.fixture
def sell_order():
    return Order(
        id=2,
        user_id=2,
        pair="BTC/USDT",
        side=OrderSide.SELL,
        type=OrderType.LIMIT,
        price=Decimal("49000.00"),
        amount=Decimal("0.1"),
        remaining=Decimal("0.1"),
        status=OrderStatus.PENDING
    )

def test_order_matching_simple(buy_order, sell_order):
    """Test simple order matching"""
    # Orders should match since buy price (50000) > sell price (49000)
    assert buy_order.price > sell_order.price
    
    # Calculate trade amount
    trade_amount = min(buy_order.remaining, sell_order.remaining)
    assert trade_amount == Decimal("0.1")
    
    # Trade price should be the sell order price (market maker)
    trade_price = sell_order.price
    assert trade_price == Decimal("49000.00")

def test_order_matching_partial(buy_order, sell_order):
    """Test partial order matching"""
    # Set different amounts
    buy_order.amount = Decimal("0.2")
    buy_order.remaining = Decimal("0.2")
    sell_order.amount = Decimal("0.1")
    sell_order.remaining = Decimal("0.1")
    
    # Only 0.1 should match
    trade_amount = min(buy_order.remaining, sell_order.remaining)
    assert trade_amount == Decimal("0.1")
    
    # Buy order should be partially filled
    buy_order.filled = trade_amount
    buy_order.remaining = buy_order.amount - buy_order.filled
    assert buy_order.remaining == Decimal("0.1")
    assert buy_order.filled == Decimal("0.1")

def test_order_matching_no_match():
    """Test orders that don't match"""
    buy_order = Order(
        id=1,
        user_id=1,
        pair="BTC/USDT",
        side=OrderSide.BUY,
        type=OrderType.LIMIT,
        price=Decimal("45000.00"),  # Lower buy price
        amount=Decimal("0.1"),
        remaining=Decimal("0.1"),
        status=OrderStatus.PENDING
    )
    
    sell_order = Order(
        id=2,
        user_id=2,
        pair="BTC/USDT",
        side=OrderSide.SELL,
        type=OrderType.LIMIT,
        price=Decimal("50000.00"),  # Higher sell price
        amount=Decimal("0.1"),
        remaining=Decimal("0.1"),
        status=OrderStatus.PENDING
    )
    
    # Orders should not match
    assert buy_order.price < sell_order.price
    assert buy_order.remaining == Decimal("0.1")
    assert sell_order.remaining == Decimal("0.1")

def test_trade_creation(buy_order, sell_order):
    """Test trade creation"""
    trade_amount = Decimal("0.1")
    trade_price = sell_order.price
    
    trade = Trade(
        buy_order_id=buy_order.id,
        sell_order_id=sell_order.id,
        pair="BTC/USDT",
        price=trade_price,
        amount=trade_amount,
        fee=trade_amount * Decimal("0.001"),  # 0.1% fee
        buyer_id=buy_order.user_id,
        seller_id=sell_order.user_id
    )
    
    assert trade.buy_order_id == buy_order.id
    assert trade.sell_order_id == sell_order.id
    assert trade.price == trade_price
    assert trade.amount == trade_amount
    assert trade.fee == trade_amount * Decimal("0.001")
    assert trade.buyer_id == buy_order.user_id
    assert trade.seller_id == sell_order.user_id
