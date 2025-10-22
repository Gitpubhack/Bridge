"""
CryptoPay API client for Bridge Exchange
"""
import httpx
import hmac
import hashlib
import json
from typing import Dict, Any, Optional
from config import CRYPTOPAY_API_TOKEN, CRYPTOPAY_API_HOST, CRYPTOPAY_WEBHOOK_SECRET, TEST_MODE

class CryptoPayClient:
    def __init__(self):
        self.api_token = CRYPTOPAY_API_TOKEN
        self.api_host = CRYPTOPAY_API_HOST
        self.webhook_secret = CRYPTOPAY_WEBHOOK_SECRET
        self.test_mode = TEST_MODE
        
    async def create_invoice(
        self, 
        asset: str, 
        amount: str, 
        description: str = "Bridge Exchange Deposit",
        paid_btn_name: str = "Open Bridge",
        paid_btn_url: str = None,
        payload: str = None
    ) -> Dict[str, Any]:
        """Create a payment invoice"""
        if self.test_mode or not self.api_token or self.api_token.startswith("TODO"):
            # Mock response for testing
            return {
                "ok": True,
                "result": {
                    "invoice_id": f"test_invoice_{hash(amount + asset)}",
                    "status": "active",
                    "hash": f"test_hash_{hash(amount + asset)}",
                    "currency_type": "crypto",
                    "asset": asset,
                    "amount": amount,
                    "description": description,
                    "created_at": "2023-01-01T00:00:00.000Z",
                    "paid_at": None,
                    "paid_btn_name": paid_btn_name,
                    "paid_btn_url": paid_btn_url or "https://t.me/bridge_exchange_bot",
                    "payload": payload
                }
            }
        
        url = f"{self.api_host}/api/invoice"
        headers = {
            "Crypto-Pay-API-Token": self.api_token,
            "Content-Type": "application/json"
        }
        
        data = {
            "asset": asset,
            "amount": amount,
            "description": description,
            "paid_btn_name": paid_btn_name,
            "paid_btn_url": paid_btn_url,
            "payload": payload
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            return response.json()
    
    async def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Get invoice status"""
        if self.test_mode or not self.api_token or self.api_token.startswith("TODO"):
            # Mock response
            return {
                "ok": True,
                "result": {
                    "invoice_id": invoice_id,
                    "status": "paid",
                    "hash": f"test_hash_{invoice_id}",
                    "currency_type": "crypto",
                    "asset": "USDT",
                    "amount": "100.00",
                    "description": "Bridge Exchange Deposit",
                    "created_at": "2023-01-01T00:00:00.000Z",
                    "paid_at": "2023-01-01T00:01:00.000Z"
                }
            }
        
        url = f"{self.api_host}/api/invoice"
        headers = {
            "Crypto-Pay-API-Token": self.api_token
        }
        params = {"invoice_ids": invoice_id}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            return response.json()
    
    async def create_transfer(
        self, 
        user_id: int, 
        asset: str, 
        amount: str, 
        spend_id: str
    ) -> Dict[str, Any]:
        """Create a transfer to user"""
        if self.test_mode or not self.api_token or self.api_token.startswith("TODO"):
            # Mock response
            return {
                "ok": True,
                "result": {
                    "transfer_id": f"test_transfer_{hash(str(user_id) + amount)}",
                    "user_id": user_id,
                    "status": "completed",
                    "transferred_at": "2023-01-01T00:00:00.000Z",
                    "comment": f"Bridge Exchange Withdrawal - {amount} {asset}"
                }
            }
        
        url = f"{self.api_host}/api/transfer"
        headers = {
            "Crypto-Pay-API-Token": self.api_token,
            "Content-Type": "application/json"
        }
        
        data = {
            "user_id": user_id,
            "asset": asset,
            "amount": amount,
            "spend_id": spend_id
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            return response.json()
    
    def verify_webhook(self, payload: str, signature: str) -> bool:
        """Verify webhook signature"""
        if self.test_mode:
            return True
            
        if not self.webhook_secret or self.webhook_secret.startswith("TODO"):
            return False
            
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    async def get_me(self) -> Dict[str, Any]:
        """Get bot information"""
        if self.test_mode or not self.api_token or self.api_token.startswith("TODO"):
            return {
                "ok": True,
                "result": {
                    "app_id": 12345,
                    "name": "Bridge Exchange Bot",
                    "payment_processing_bot_username": "bridge_exchange_bot"
                }
            }
        
        url = f"{self.api_host}/api/getMe"
        headers = {
            "Crypto-Pay-API-Token": self.api_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json()
