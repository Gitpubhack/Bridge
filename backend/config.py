"""
Bridge Exchange Configuration
All secrets should be set via environment variables or .env file
"""
import os
from decimal import Decimal
from typing import Optional

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bridge.db")

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TODO_TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "TODO_WEBHOOK_SECRET")

# CryptoPay Integration
CRYPTOPAY_API_TOKEN = os.getenv("CRYPTOPAY_API_TOKEN", "TODO_CRYPTOPAY_TOKEN")
CRYPTOPAY_API_HOST = os.getenv("CRYPTOPAY_API_HOST", "https://pay.crypt.bot")
CRYPTOPAY_WEBHOOK_SECRET = os.getenv("CRYPTOPAY_WEBHOOK_SECRET", "TODO_CRYPTOPAY_WEBHOOK")

# Bybit Integration
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "TODO_BYBIT_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "TODO_BYBIT_SECRET")
BYBIT_TESTNET = os.getenv("BYBIT_TESTNET", "true").lower() == "true"

# TON Integration
TONAPI_KEY = os.getenv("TONAPI_KEY", "TODO_TONAPI_KEY")
TONAPI_BASE_URL = os.getenv("TONAPI_BASE_URL", "https://tonapi.io")

# CoinGecko API
GECKO_API_KEY = os.getenv("GECKO_API_KEY", "TODO_GECKO_KEY")
GECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# OpenAI Integration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "TODO_OPENAI_KEY")

# JWT Settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Application Settings
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
NGROK_URL = os.getenv("NGROK_URL", "")

# Exchange Settings
DEFAULT_FEE_RATE = Decimal("0.001")  # 0.1%
MINIMUM_ORDER_SIZE = Decimal("0.001")
MAXIMUM_ORDER_SIZE = Decimal("1000000")

# Supported Assets
SUPPORTED_CRYPTO_ASSETS = [
    "BTC", "ETH", "USDT", "USDC", "TON", "BNB", "ADA", "SOL", "DOT", "MATIC"
]

SUPPORTED_FIAT_ASSETS = [
    "USD", "EUR", "RUB", "UAH", "KZT", "TRY"
]

# Trading Pairs
DEFAULT_TRADING_PAIRS = [
    "BTC/USDT", "ETH/USDT", "TON/USDT", "BNB/USDT", "ADA/USDT"
]

# Security Settings
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15
RATE_LIMIT_PER_MINUTE = 60

# Background Jobs
INVOICE_POLLING_INTERVAL = 30  # seconds
PRICE_UPDATE_INTERVAL = 10  # seconds
RECONCILE_INTERVAL = 300  # seconds

# Admin Settings
ADMIN_TELEGRAM_IDS = [
    int(x) for x in os.getenv("ADMIN_TELEGRAM_IDS", "").split(",") if x.strip()
]

# Notification Settings
SEND_TELEGRAM_NOTIFICATIONS = os.getenv("SEND_TELEGRAM_NOTIFICATIONS", "true").lower() == "true"

# CORS Settings
ALLOWED_ORIGINS = [
    "https://web.telegram.org",
    "https://t.me",
    "http://localhost:3000",
    "http://localhost:8080",
]

if NGROK_URL:
    ALLOWED_ORIGINS.append(NGROK_URL)

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
