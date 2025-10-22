"""
CoinGecko API client for Bridge Exchange
"""
import httpx
from typing import Dict, Any, Optional, List
from config import GECKO_API_KEY, GECKO_BASE_URL, TEST_MODE

class GeckoClient:
    def __init__(self):
        self.api_key = GECKO_API_KEY
        self.base_url = GECKO_BASE_URL
        self.test_mode = TEST_MODE
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        headers = {"Content-Type": "application/json"}
        if self.api_key and not self.api_key.startswith("TODO"):
            headers["x-cg-demo-api-key"] = self.api_key
        return headers
    
    async def get_price(
        self, 
        ids: List[str], 
        vs_currencies: List[str] = ["usd"],
        include_market_cap: bool = True,
        include_24hr_vol: bool = True,
        include_24hr_change: bool = True
    ) -> Dict[str, Any]:
        """Get cryptocurrency prices"""
        if self.test_mode:
            # Mock price data
            prices = {}
            for coin_id in ids:
                prices[coin_id] = {
                    "usd": 50000.0 if coin_id == "bitcoin" else 3000.0 if coin_id == "ethereum" else 1.0,
                    "usd_market_cap": 1000000000000 if coin_id == "bitcoin" else 300000000000,
                    "usd_24h_vol": 20000000000 if coin_id == "bitcoin" else 10000000000,
                    "usd_24h_change": 2.5 if coin_id == "bitcoin" else -1.2
                }
            return prices
        
        url = f"{self.base_url}/simple/price"
        params = {
            "ids": ",".join(ids),
            "vs_currencies": ",".join(vs_currencies),
            "include_market_cap": include_market_cap,
            "include_24hr_vol": include_24hr_vol,
            "include_24hr_change": include_24hr_change
        }
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            return response.json()
    
    async def get_coin_list(self, include_platform: bool = False) -> List[Dict[str, Any]]:
        """Get list of all coins"""
        if self.test_mode:
            return [
                {
                    "id": "bitcoin",
                    "symbol": "btc",
                    "name": "Bitcoin",
                    "platforms": {}
                },
                {
                    "id": "ethereum",
                    "symbol": "eth", 
                    "name": "Ethereum",
                    "platforms": {}
                },
                {
                    "id": "tether",
                    "symbol": "usdt",
                    "name": "Tether",
                    "platforms": {}
                }
            ]
        
        url = f"{self.base_url}/coins/list"
        params = {"include_platform": include_platform}
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            return response.json()
    
    async def get_coin_market_data(
        self, 
        vs_currency: str = "usd",
        order: str = "market_cap_desc",
        per_page: int = 100,
        page: int = 1,
        sparkline: bool = False,
        price_change_percentage: str = "24h"
    ) -> List[Dict[str, Any]]:
        """Get market data for coins"""
        if self.test_mode:
            return [
                {
                    "id": "bitcoin",
                    "symbol": "btc",
                    "name": "Bitcoin",
                    "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
                    "current_price": 50000.0,
                    "market_cap": 1000000000000,
                    "market_cap_rank": 1,
                    "fully_diluted_valuation": 1050000000000,
                    "total_volume": 20000000000,
                    "high_24h": 51000.0,
                    "low_24h": 49000.0,
                    "price_change_24h": 1000.0,
                    "price_change_percentage_24h": 2.04,
                    "market_cap_change_24h": 20000000000,
                    "market_cap_change_percentage_24h": 2.04,
                    "circulating_supply": 20000000.0,
                    "total_supply": 21000000.0,
                    "max_supply": 21000000.0,
                    "ath": 69000.0,
                    "ath_change_percentage": -27.54,
                    "ath_date": "2021-11-10T14:24:11.849Z",
                    "atl": 67.81,
                    "atl_change_percentage": 73630.0,
                    "atl_date": "2013-07-06T00:00:00.000Z",
                    "roi": None,
                    "last_updated": "2023-01-01T00:00:00.000Z"
                }
            ]
        
        url = f"{self.base_url}/coins/markets"
        params = {
            "vs_currency": vs_currency,
            "order": order,
            "per_page": per_page,
            "page": page,
            "sparkline": sparkline,
            "price_change_percentage": price_change_percentage
        }
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            return response.json()
    
    async def get_coin_by_id(self, coin_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific coin"""
        if self.test_mode:
            return {
                "id": coin_id,
                "symbol": coin_id,
                "name": coin_id.title(),
                "description": {
                    "en": f"Description for {coin_id}"
                },
                "market_data": {
                    "current_price": {"usd": 50000.0},
                    "market_cap": {"usd": 1000000000000},
                    "total_volume": {"usd": 20000000000},
                    "high_24h": {"usd": 51000.0},
                    "low_24h": {"usd": 49000.0},
                    "price_change_24h": 1000.0,
                    "price_change_percentage_24h": 2.04,
                    "market_cap_change_24h": 20000000000,
                    "market_cap_change_percentage_24h": 2.04
                }
            }
        
        url = f"{self.base_url}/coins/{coin_id}"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json()
    
    async def get_trending_coins(self) -> Dict[str, Any]:
        """Get trending coins"""
        if self.test_mode:
            return {
                "coins": [
                    {
                        "item": {
                            "id": "bitcoin",
                            "coin_id": 1,
                            "name": "Bitcoin",
                            "symbol": "BTC",
                            "market_cap_rank": 1,
                            "thumb": "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png",
                            "small": "https://assets.coingecko.com/coins/images/1/small/bitcoin.png",
                            "large": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
                            "slug": "bitcoin",
                            "price_btc": 1.0,
                            "score": 0
                        }
                    }
                ]
            }
        
        url = f"{self.base_url}/search/trending"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json()
