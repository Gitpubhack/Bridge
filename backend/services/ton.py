"""
TON API client for Bridge Exchange
"""
import httpx
from typing import Dict, Any, Optional
from config import TONAPI_KEY, TONAPI_BASE_URL, TEST_MODE

class TONClient:
    def __init__(self):
        self.api_key = TONAPI_KEY
        self.base_url = TONAPI_BASE_URL
        self.test_mode = TEST_MODE
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        headers = {"Content-Type": "application/json"}
        if self.api_key and not self.api_key.startswith("TODO"):
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    async def get_account_info(self, address: str) -> Dict[str, Any]:
        """Get account information"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "balance": "1000000000",  # 1 TON in nanotons
                "state": "active",
                "last_activity": 1640995200,
                "frozen": False,
                "code": None,
                "data": None
            }
        
        url = f"{self.base_url}/v2/accounts/{address}"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json()
    
    async def get_jetton_balances(self, address: str) -> Dict[str, Any]:
        """Get jetton balances for an account"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "balances": [
                    {
                        "balance": "1000000000",
                        "price": {
                            "prices": [
                                {
                                    "source": "coinmarketcap",
                                    "price": "2.50"
                                }
                            ]
                        },
                        "jetton": {
                            "address": "EQD0vdSA_NedR9uvnhdRqM5eK9Oat1yp_B-MQcgT1xQ_buFD",
                            "name": "Tether USD",
                            "symbol": "USDT",
                            "decimals": 6,
                            "image": "https://tonapi.io/img/jetton/USDT.png",
                            "description": "Tether USD"
                        }
                    }
                ]
            }
        
        url = f"{self.base_url}/v2/accounts/{address}/jettons"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json()
    
    async def mint_nft(
        self, 
        owner_address: str, 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Mint an NFT"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "ok": True,
                "result": {
                    "token_id": f"test_nft_{hash(str(metadata))}",
                    "transaction_hash": f"test_tx_{hash(str(metadata))}",
                    "owner_address": owner_address
                }
            }
        
        url = f"{self.base_url}/v2/nfts/mint"
        headers = self._get_headers()
        data = {
            "owner_address": owner_address,
            "metadata": metadata
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            return response.json()
    
    async def get_nft_info(self, token_id: str) -> Dict[str, Any]:
        """Get NFT information"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "address": token_id,
                "index": "0",
                "owner": {
                    "address": "EQD0vdSA_NedR9uvnhdRqM5eK9Oat1yp_B-MQcgT1xQ_buFD",
                    "is_scam": False,
                    "is_wallet": True
                },
                "collection": {
                    "address": "EQD0vdSA_NedR9uvnhdRqM5eK9Oat1yp_B-MQcgT1xQ_buFD",
                    "name": "Bridge Exchange NFTs",
                    "description": "Official Bridge Exchange NFT Collection"
                },
                "verified": True,
                "metadata": {
                    "name": "Bridge NFT #1",
                    "description": "A unique NFT from Bridge Exchange",
                    "image": "https://bridge.exchange/nft/1.png"
                },
                "sale": None,
                "previews": [
                    {
                        "resolution": "100x100",
                        "url": "https://bridge.exchange/nft/1_100x100.png"
                    }
                ]
            }
        
        url = f"{self.base_url}/v2/nfts/{token_id}"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json()
    
    async def transfer_nft(
        self, 
        token_id: str, 
        from_address: str, 
        to_address: str
    ) -> Dict[str, Any]:
        """Transfer NFT"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "ok": True,
                "result": {
                    "transaction_hash": f"test_transfer_{hash(token_id + to_address)}",
                    "from_address": from_address,
                    "to_address": to_address,
                    "token_id": token_id
                }
            }
        
        url = f"{self.base_url}/v2/nfts/{token_id}/transfer"
        headers = self._get_headers()
        data = {
            "from_address": from_address,
            "to_address": to_address
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            return response.json()
    
    async def get_rates(self) -> Dict[str, Any]:
        """Get TON rates"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "rates": {
                    "TON": {
                        "prices": [
                            {
                                "source": "coinmarketcap",
                                "price": "2.50"
                            }
                        ]
                    }
                }
            }
        
        url = f"{self.base_url}/v2/rates"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json()
