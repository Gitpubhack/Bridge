"""
Example configuration file for Bridge Exchange
Copy this to config.py and fill in your actual API keys
"""
import os
from decimal import Decimal

# Database
DATABASE_URL = "sqlite+aiosqlite:///./bridge.db"

# Telegram Bot (Get from @BotFather)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_WEBHOOK_SECRET = "YOUR_WEBHOOK_SECRET"

# CryptoPay Integration (Get from https://crypt.bot)
CRYPTOPAY_API_TOKEN = "YOUR_CRYPTOPAY_TOKEN"
CRYPTOPAY_API_HOST = "https://pay.crypt.bot"
CRYPTOPAY_WEBHOOK_SECRET = "YOUR_CRYPTOPAY_WEBHOOK_SECRET"

# Bybit Integration (Get from Bybit API)
BYBIT_API_KEY = "YOUR_BYBIT_API_KEY"
BYBIT_API_SECRET = "YOUR_BYBIT_API_SECRET"
BYBIT_TESTNET = True  # Set to False for mainnet

# TON Integration (Get from https://tonapi.io)
TONAPI_KEY = "YOUR_TONAPI_KEY"
TONAPI_BASE_URL = "https://tonapi.io"

# CoinGecko API (Optional, for price data)
GECKO_API_KEY = "YOUR_GECKO_API_KEY"

# OpenAI Integration (Get from OpenAI)
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# JWT Settings
JWT_SECRET_KEY = "your-very-secure-secret-key-change-this"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Application Settings
TEST_MODE = True  # Set to False for production
DEBUG = True
NGROK_URL = ""  # Will be set when you run ngrok

# Admin Settings (Telegram IDs of admins)
ADMIN_TELEGRAM_IDS = [123456789, 987654321]  # Replace with actual admin IDs

# Notification Settings
SEND_TELEGRAM_NOTIFICATIONS = True
