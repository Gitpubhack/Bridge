"""
Bybit API client for Bridge Exchange
"""
import httpx
import hmac
import hashlib
import time
import json
from typing import Dict, Any, Optional, List
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_TESTNET, TEST_MODE

class BybitClient:
    def __init__(self):
        self.api_key = BYBIT_API_KEY
        self.api_secret = BYBIT_API_SECRET
        self.testnet = BYBIT_TESTNET
        self.test_mode = TEST_MODE
        
        if self.testnet:
            self.base_url = "https://api-testnet.bybit.com"
        else:
            self.base_url = "https://api.bybit.com"
    
    def _generate_signature(self, params: str, timestamp: str) -> str:
        """Generate API signature"""
        if self.test_mode or not self.api_secret or self.api_secret.startswith("TODO"):
            return "test_signature"
            
        param_str = f"{timestamp}{self.api_key}{params}"
        return hmac.new(
            self.api_secret.encode(),
            param_str.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _get_headers(self, params: str = "") -> Dict[str, str]:
        """Get request headers with signature"""
        timestamp = str(int(time.time() * 1000))
        signature = self._generate_signature(params, timestamp)
        
        return {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }
    
    async def get_server_time(self) -> Dict[str, Any]:
        """Get server time"""
        if self.test_mode:
            return {
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "timeSecond": str(int(time.time())),
                    "timeNano": str(int(time.time() * 1000000000))
                }
            }
        
        url = f"{self.base_url}/v5/market/time"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
    
    async def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get ticker information"""
        if self.test_mode:
            # Mock ticker data
            return {
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "list": [{
                        "symbol": symbol,
                        "lastPrice": "50000.00",
                        "indexPrice": "50000.00",
                        "markPrice": "50000.00",
                        "prevPrice24h": "49000.00",
                        "price24hPcnt": "0.0204",
                        "highPrice24h": "51000.00",
                        "lowPrice24h": "49000.00",
                        "prevPrice1h": "49500.00",
                        "openInterest": "1000000.00",
                        "openInterestValue": "50000000000.00",
                        "turnover24h": "1000000000.00",
                        "volume24h": "20000.00",
                        "nextFundingTime": "2023-01-01T00:00:00.000Z",
                        "fundingRate": "0.0001",
                        "bid1Price": "49999.00",
                        "ask1Price": "50001.00",
                        "bid1Size": "1.00",
                        "ask1Size": "1.00"
                    }]
                }
            }
        
        url = f"{self.base_url}/v5/market/tickers"
        params = {"category": "spot", "symbol": symbol}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return response.json()
    
    async def get_orderbook(self, symbol: str, limit: int = 25) -> Dict[str, Any]:
        """Get order book"""
        if self.test_mode:
            # Mock order book data
            bids = [{"0": "49999.00", "1": "1.00"} for _ in range(10)]
            asks = [{"0": "50001.00", "1": "1.00"} for _ in range(10)]
            
            return {
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "s": symbol,
                    "b": bids,
                    "a": asks,
                    "ts": int(time.time() * 1000),
                    "u": 1
                }
            }
        
        url = f"{self.base_url}/v5/market/orderbook"
        params = {"category": "spot", "symbol": symbol, "limit": limit}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return response.json()
    
    async def get_account_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "list": [
                        {
                            "accountType": "UNIFIED",
                            "accountId": "test_account",
                            "memberId": "test_member",
                            "balance": [
                                {
                                    "coin": "USDT",
                                    "walletBalance": "10000.00",
                                    "transferBalance": "0.00"
                                },
                                {
                                    "coin": "BTC",
                                    "walletBalance": "0.1",
                                    "transferBalance": "0.0"
                                }
                            ]
                        }
                    ]
                }
            }
        
        url = f"{self.base_url}/v5/account/wallet-balance"
        params = {"accountType": "UNIFIED"}
        headers = self._get_headers(json.dumps(params))
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            return response.json()
    
    async def place_order(
        self, 
        symbol: str, 
        side: str, 
        order_type: str, 
        qty: str, 
        price: Optional[str] = None
    ) -> Dict[str, Any]:
        """Place an order"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "orderId": f"test_order_{int(time.time())}",
                    "orderLinkId": f"bridge_{int(time.time())}"
                }
            }
        
        url = f"{self.base_url}/v5/order/create"
        data = {
            "category": "spot",
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "qty": qty,
            "price": price,
            "timeInForce": "GTC"
        }
        
        headers = self._get_headers(json.dumps(data))
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            return response.json()
    
    async def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """Cancel an order"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "orderId": order_id,
                    "orderLinkId": f"bridge_{order_id}"
                }
            }
        
        url = f"{self.base_url}/v5/order/cancel"
        data = {
            "category": "spot",
            "symbol": symbol,
            "orderId": order_id
        }
        
        headers = self._get_headers(json.dumps(data))
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            return response.json()
    
    async def get_open_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get open orders"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "list": []
                }
            }
        
        url = f"{self.base_url}/v5/order/realtime"
        params = {"category": "spot"}
        if symbol:
            params["symbol"] = symbol
        
        headers = self._get_headers(json.dumps(params))
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            return response.json()
