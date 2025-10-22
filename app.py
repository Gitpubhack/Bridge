"""
Bridge Exchange - Простое приложение
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Создаем приложение
app = FastAPI(
    title="Bridge Exchange",
    description="Криптовалютная биржа с Telegram интеграцией",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Главная страница"""
    return {
        "message": "🚀 Bridge Exchange работает!",
        "status": "OK",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "test": "/api/test",
            "wallet": "/api/wallet/balances/1",
            "exchange": "/api/exchange/orderbook"
        }
    }

@app.get("/health")
async def health():
    """Проверка здоровья"""
    return {
        "status": "healthy",
        "message": "Сервер работает нормально"
    }

@app.get("/api/test")
async def test():
    """Тестовый эндпоинт"""
    return {
        "message": "✅ API работает!",
        "data": {
            "user_id": 1,
            "balance": "1000 USDT",
            "btc_balance": "0.05 BTC"
        }
    }

@app.get("/api/wallet/balances/{user_id}")
async def get_balances(user_id: int):
    """Получить балансы пользователя"""
    return {
        "user_id": user_id,
        "balances": {
            "USDT": {"amount": "1000.00", "reserved": "0.00"},
            "BTC": {"amount": "0.05", "reserved": "0.00"},
            "ETH": {"amount": "2.5", "reserved": "0.00"}
        }
    }

@app.post("/api/wallet/deposit")
async def deposit():
    """Создать депозит"""
    return {
        "invoice_id": "inv_123456",
        "pay_url": "https://pay.crypt.bot/pay/inv_123456",
        "status": "pending",
        "amount": "100.00",
        "asset": "USDT"
    }

@app.get("/api/exchange/orderbook")
async def get_orderbook(pair: str = "BTC/USDT"):
    """Получить стакан заявок"""
    return {
        "pair": pair,
        "bids": [
            {"price": "50000.00", "amount": "0.1"},
            {"price": "49999.00", "amount": "0.2"}
        ],
        "asks": [
            {"price": "50001.00", "amount": "0.1"},
            {"price": "50002.00", "amount": "0.2"}
        ],
        "last_price": "50000.50"
    }

@app.post("/api/exchange/order")
async def place_order():
    """Разместить ордер"""
    return {
        "order_id": "ord_123456",
        "status": "pending",
        "pair": "BTC/USDT",
        "side": "buy",
        "price": "50000.00",
        "amount": "0.1"
    }

@app.get("/api/nft/listings")
async def get_nft_listings():
    """Получить NFT листинги"""
    return {
        "listings": [
            {
                "id": 1,
                "name": "Cool NFT #1",
                "price": "100.00 USDT",
                "owner": "user123"
            }
        ]
    }

@app.get("/api/ai/portfolio/{user_id}")
async def get_portfolio_advice(user_id: int):
    """Получить AI советы по портфелю"""
    return {
        "user_id": user_id,
        "risk_level": "medium",
        "suggestions": [
            "Рассмотрите диверсификацию портфеля",
            "BTC показывает сильный потенциал",
            "Мониторьте волатильность рынка"
        ]
    }

if __name__ == "__main__":
    print("🚀 Запуск Bridge Exchange...")
    print("📱 API будет доступен на: http://localhost:8003")
    print("📚 Документация: http://localhost:8003/docs")
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
