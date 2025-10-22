"""
Tests for CryptoPay integration
"""
import pytest
from unittest.mock import AsyncMock, patch
from services.cryptopay import CryptoPayClient

@pytest.fixture
def cryptopay_client():
    return CryptoPayClient()

@pytest.mark.asyncio
async def test_create_invoice_mock_mode(cryptopay_client):
    """Test invoice creation in mock mode"""
    cryptopay_client.test_mode = True
    
    result = await cryptopay_client.create_invoice(
        asset="USDT",
        amount="100.00",
        description="Test deposit"
    )
    
    assert result["ok"] is True
    assert "result" in result
    assert result["result"]["asset"] == "USDT"
    assert result["result"]["amount"] == "100.00"

@pytest.mark.asyncio
async def test_get_invoice_mock_mode(cryptopay_client):
    """Test getting invoice status in mock mode"""
    cryptopay_client.test_mode = True
    
    result = await cryptopay_client.get_invoice("test_invoice_123")
    
    assert result["ok"] is True
    assert result["result"]["status"] == "paid"

@pytest.mark.asyncio
async def test_verify_webhook_mock_mode(cryptopay_client):
    """Test webhook verification in mock mode"""
    cryptopay_client.test_mode = True
    
    is_valid = cryptopay_client.verify_webhook("test_payload", "test_signature")
    assert is_valid is True

@pytest.mark.asyncio
async def test_create_transfer_mock_mode(cryptopay_client):
    """Test transfer creation in mock mode"""
    cryptopay_client.test_mode = True
    
    result = await cryptopay_client.create_transfer(
        user_id=123456789,
        asset="USDT",
        amount="50.00",
        spend_id="test_spend_123"
    )
    
    assert result["ok"] is True
    assert result["result"]["user_id"] == 123456789
    assert result["result"]["status"] == "completed"
