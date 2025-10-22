#!/usr/bin/env python3
"""
Bridge Exchange Demo Flow
Simulates a complete user journey: deposit -> trade -> withdraw
"""
import asyncio
import httpx
import json
from decimal import Decimal
from datetime import datetime

# Configuration
API_BASE = "http://localhost:8000/api"
TEST_USER_DATA = {
    "webapp_data": json.dumps({
        "initData": "test_data",
        "hash": "test_hash"
    })
}

class BridgeDemo:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.access_token = None
        self.user_id = None
        self.invoice_id = None
        self.order_id = None
        self.transaction_id = None
    
    async def run_demo(self):
        """Run the complete demo flow"""
        print("🚀 Starting Bridge Exchange Demo Flow")
        print("=" * 50)
        
        try:
            # Step 1: Login
            await self.login()
            
            # Step 2: Create deposit
            await self.create_deposit()
            
            # Step 3: Simulate webhook payment
            await self.simulate_payment()
            
            # Step 4: Check balances
            await self.check_balances()
            
            # Step 5: Place trade order
            await self.place_trade_order()
            
            # Step 6: Get AI analysis
            await self.get_ai_analysis()
            
            # Step 7: Create withdrawal
            await self.create_withdrawal()
            
            print("\n✅ Demo completed successfully!")
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
        finally:
            await self.client.aclose()
    
    async def login(self):
        """Step 1: Login with Telegram"""
        print("\n1️⃣ Logging in with Telegram...")
        
        response = await self.client.post(
            f"{API_BASE}/auth/telegram_login",
            json=TEST_USER_DATA
        )
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.user_id = data["user"]["id"]
            print(f"✅ Logged in as user {self.user_id}")
        else:
            raise Exception(f"Login failed: {response.text}")
    
    async def create_deposit(self):
        """Step 2: Create deposit invoice"""
        print("\n2️⃣ Creating deposit invoice...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        deposit_data = {
            "user_id": self.user_id,
            "asset": "USDT",
            "amount": "100.00"
        }
        
        response = await self.client.post(
            f"{API_BASE}/wallet/deposit",
            json=deposit_data,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            self.invoice_id = data["invoice_id"]
            print(f"✅ Created deposit invoice {self.invoice_id}")
            print(f"   Pay URL: {data['pay_url']}")
        else:
            raise Exception(f"Deposit creation failed: {response.text}")
    
    async def simulate_payment(self):
        """Step 3: Simulate CryptoPay webhook payment"""
        print("\n3️⃣ Simulating payment webhook...")
        
        webhook_data = {
            "invoice_id": f"test_invoice_{self.invoice_id}",
            "status": "paid",
            "amount": "100.00",
            "asset": "USDT"
        }
        
        response = await self.client.post(
            f"{API_BASE}/wallet/crypto/webhook",
            json=webhook_data
        )
        
        if response.status_code == 200:
            print("✅ Payment processed successfully")
        else:
            print(f"⚠️ Webhook response: {response.text}")
    
    async def check_balances(self):
        """Step 4: Check user balances"""
        print("\n4️⃣ Checking balances...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = await self.client.get(
            f"{API_BASE}/wallet/balances/{self.user_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Current balances:")
            for balance in data["balances"]:
                print(f"   {balance['asset']}: {balance['amount']} (Available: {balance['available']})")
        else:
            print(f"⚠️ Balance check failed: {response.text}")
    
    async def place_trade_order(self):
        """Step 5: Place a trade order"""
        print("\n5️⃣ Placing trade order...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        order_data = {
            "user_id": self.user_id,
            "pair": "BTC/USDT",
            "side": "buy",
            "type": "market",
            "amount": "0.001",
            "immediate_fill": True
        }
        
        response = await self.client.post(
            f"{API_BASE}/exchange/order",
            json=order_data,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            self.order_id = data["order_id"]
            print(f"✅ Order placed: {data['order_id']}")
            print(f"   Status: {data['status']}")
            print(f"   Filled: {data['filled']}")
        else:
            print(f"⚠️ Order placement failed: {response.text}")
    
    async def get_ai_analysis(self):
        """Step 6: Get AI portfolio analysis"""
        print("\n6️⃣ Getting AI portfolio analysis...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = await self.client.post(
            f"{API_BASE}/ai/portfolio",
            json={"user_id": self.user_id},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ AI Analysis:")
            print(f"   Risk Level: {data['risk_level']}")
            print(f"   Total Value: ${data['total_value_usd']}")
            print("   Suggestions:")
            for suggestion in data['suggestions']:
                print(f"     - {suggestion['title']}: {suggestion['description']}")
        else:
            print(f"⚠️ AI analysis failed: {response.text}")
    
    async def create_withdrawal(self):
        """Step 7: Create withdrawal request"""
        print("\n7️⃣ Creating withdrawal request...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        withdrawal_data = {
            "user_id": self.user_id,
            "asset": "USDT",
            "amount": "50.00",
            "to_address": "0x1234567890123456789012345678901234567890"
        }
        
        response = await self.client.post(
            f"{API_BASE}/wallet/withdraw",
            json=withdrawal_data,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            self.transaction_id = data["transaction_id"]
            print(f"✅ Withdrawal created: {data['transaction_id']}")
            print(f"   Amount: {data['amount']} {data['asset']}")
            print(f"   Fee: {data['fee']} {data['asset']}")
        else:
            print(f"⚠️ Withdrawal creation failed: {response.text}")
    
    async def test_additional_features(self):
        """Test additional features"""
        print("\n🔧 Testing additional features...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test NFT minting
        try:
            nft_data = {
                "user_id": self.user_id,
                "metadata": {
                    "name": "Bridge Demo NFT",
                    "description": "A demo NFT from Bridge Exchange",
                    "image": "https://bridge.exchange/demo-nft.png"
                }
            }
            
            response = await self.client.post(
                f"{API_BASE}/nft/mint",
                json=nft_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ NFT minted successfully")
            else:
                print(f"⚠️ NFT minting failed: {response.text}")
        except Exception as e:
            print(f"⚠️ NFT test failed: {e}")
        
        # Test P2P offer
        try:
            p2p_data = {
                "seller_id": self.user_id,
                "asset": "USDT",
                "amount": "25.00",
                "price": "1.00",
                "payment_method": "Bank Transfer"
            }
            
            response = await self.client.post(
                f"{API_BASE}/p2p/offer",
                json=p2p_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ P2P offer created successfully")
            else:
                print(f"⚠️ P2P offer failed: {response.text}")
        except Exception as e:
            print(f"⚠️ P2P test failed: {e}")
        
        # Test staking
        try:
            stake_data = {
                "user_id": self.user_id,
                "asset": "USDT",
                "amount": "10.00",
                "duration_days": 30
            }
            
            response = await self.client.post(
                f"{API_BASE}/stake/stake",
                json=stake_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Staking created successfully")
            else:
                print(f"⚠️ Staking failed: {response.text}")
        except Exception as e:
            print(f"⚠️ Staking test failed: {e}")

async def main():
    """Main demo function"""
    demo = BridgeDemo()
    await demo.run_demo()
    
    # Test additional features
    await demo.test_additional_features()

if __name__ == "__main__":
    print("Bridge Exchange Demo Flow")
    print("Make sure the backend is running on http://localhost:8000")
    print("Press Ctrl+C to cancel")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
