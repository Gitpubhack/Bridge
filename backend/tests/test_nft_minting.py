"""
Tests for NFT minting functionality
"""
import pytest
from unittest.mock import AsyncMock, patch
from services.ton import TONClient

@pytest.fixture
def ton_client():
    return TONClient()

@pytest.mark.asyncio
async def test_mint_nft_mock_mode(ton_client):
    """Test NFT minting in mock mode"""
    ton_client.test_mode = True
    
    metadata = {
        "name": "Test NFT",
        "description": "A test NFT",
        "image": "https://example.com/image.png"
    }
    
    result = await ton_client.mint_nft(
        owner_address="EQD0vdSA_NedR9uvnhdRqM5eK9Oat1yp_B-MQcgT1xQ_buFD",
        metadata=metadata
    )
    
    assert result["ok"] is True
    assert "result" in result
    assert "token_id" in result["result"]
    assert "transaction_hash" in result["result"]
    assert result["result"]["owner_address"] == "EQD0vdSA_NedR9uvnhdRqM5eK9Oat1yp_B-MQcgT1xQ_buFD"

@pytest.mark.asyncio
async def test_get_nft_info_mock_mode(ton_client):
    """Test getting NFT info in mock mode"""
    ton_client.test_mode = True
    
    result = await ton_client.get_nft_info("test_token_123")
    
    assert "address" in result
    assert "owner" in result
    assert "metadata" in result
    assert result["verified"] is True

@pytest.mark.asyncio
async def test_transfer_nft_mock_mode(ton_client):
    """Test NFT transfer in mock mode"""
    ton_client.test_mode = True
    
    result = await ton_client.transfer_nft(
        token_id="test_token_123",
        from_address="EQD0vdSA_NedR9uvnhdRqM5eK9Oat1yp_B-MQcgT1xQ_buFD",
        to_address="EQD0vdSA_NedR9uvnhdRqM5eK9Oat1yp_B-MQcgT1xQ_buFE"
    )
    
    assert result["ok"] is True
    assert "result" in result
    assert result["result"]["token_id"] == "test_token_123"
    assert "transaction_hash" in result["result"]

@pytest.mark.asyncio
async def test_get_account_info_mock_mode(ton_client):
    """Test getting account info in mock mode"""
    ton_client.test_mode = True
    
    result = await ton_client.get_account_info("EQD0vdSA_NedR9uvnhdRqM5eK9Oat1yp_B-MQcgT1xQ_buFD")
    
    assert "balance" in result
    assert "state" in result
    assert result["state"] == "active"
    assert result["frozen"] is False
