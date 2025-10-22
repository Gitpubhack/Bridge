# Bridge Exchange

A fully functional, local-testable, modular hybrid crypto exchange Mini App for Telegram. This production-grade system includes wallets, exchange, P2P escrow, NFT marketplace, staking, DAO, referral system, admin panel, support tickets, and AI assistant.

## 🚀 Features

### Core Functionality
- **Telegram Mini App** - Native WebApp integration
- **Multi-Asset Wallets** - CryptoPay integration for deposits/withdrawals
- **Hybrid Exchange** - Internal orderbook + Bybit/DEX fallback
- **P2P Trading** - Escrow-based peer-to-peer trading
- **NFT Marketplace** - Mint, trade, and manage NFTs
- **Staking & Farming** - Lock tokens for rewards
- **DAO Governance** - Community-driven decision making
- **AI Assistant** - OpenAI-powered portfolio analysis
- **Admin Panel** - Complete management interface
- **Support System** - Ticket-based customer support

### Technical Stack
- **Backend**: FastAPI + SQLAlchemy + Alembic
- **Database**: SQLite (PostgreSQL-ready)
- **Frontend**: Vanilla JS + Telegram WebApp API
- **External APIs**: CryptoPay, Bybit, TON, CoinGecko, OpenAI
- **Security**: JWT authentication, webhook verification
- **Background Jobs**: APScheduler for periodic tasks

## 📁 Project Structure

```
/bridge/
├─ backend/
│ ├─ main.py                 # FastAPI application
│ ├─ config.py               # Configuration settings
│ ├─ database.py             # Database connection
│ ├─ alembic/                # Database migrations
│ ├─ models/                 # SQLAlchemy models
│ ├─ schemas/                # Pydantic schemas
│ ├─ services/               # External API clients
│ ├─ routers/                # API endpoints
│ ├─ tasks.py                # Background jobs
│ └─ tests/                  # Test suite
├─ frontend/                 # Telegram WebApp
│ ├─ index.html
│ ├─ assets/
│ │ ├─ styles.css
│ │ └─ script.js
├─ scripts/
│ ├─ demo_flow.py            # Demo simulation
│ └─ run_ngrok.sh            # Ngrok setup
├─ README.md
└─ config.example.py
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (for frontend development)
- ngrok (for Telegram WebApp testing)
- Telegram Bot Token
- API Keys (see Configuration section)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd bridge
```

### 2. Backend Setup

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Copy configuration
cp backend/config.example.py backend/config.py

# Edit configuration with your API keys
nano backend/config.py

# Initialize database
cd backend
alembic upgrade head

# Start backend server
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
# No build process needed - static files
# Serve frontend files from /frontend directory
```

### 4. Ngrok Setup (for Telegram WebApp)

```bash
# Make script executable
chmod +x scripts/run_ngrok.sh

# Start ngrok tunnel
./scripts/run_ngrok.sh 8000

# Update config.py with the ngrok URL
# NGROK_URL = "https://your-ngrok-url.ngrok.io"
```

## 🔧 Configuration

Edit `backend/config.py` with your API keys:

```python
# Telegram Bot
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# CryptoPay Integration
CRYPTOPAY_API_TOKEN = "YOUR_CRYPTOPAY_TOKEN"
CRYPTOPAY_WEBHOOK_SECRET = "YOUR_WEBHOOK_SECRET"

# Bybit Integration
BYBIT_API_KEY = "YOUR_BYBIT_API_KEY"
BYBIT_API_SECRET = "YOUR_BYBIT_API_SECRET"

# TON Integration
TONAPI_KEY = "YOUR_TONAPI_KEY"

# OpenAI Integration
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# Admin Settings
ADMIN_TELEGRAM_IDS = [123456789, 987654321]
```

### Required API Keys

1. **Telegram Bot Token** - Get from @BotFather
2. **CryptoPay Token** - Get from https://crypt.bot
3. **Bybit API Keys** - Get from Bybit API settings
4. **TON API Key** - Get from https://tonapi.io
5. **OpenAI API Key** - Get from OpenAI platform

## 🧪 Testing

### Run Demo Flow

```bash
# Make sure backend is running on port 8000
python scripts/demo_flow.py
```

### Run Unit Tests

```bash
cd backend
pytest tests/ -v
```

### Test Coverage

```bash
pytest tests/ --cov=backend --cov-report=html
```

## 📱 Telegram WebApp Setup

### 1. Create Telegram Bot

1. Message @BotFather on Telegram
2. Create new bot with `/newbot`
3. Get your bot token
4. Set WebApp URL: `https://your-ngrok-url.ngrok.io/frontend/`

### 2. Configure WebApp

```javascript
// In your bot, send this message to users:
const webAppUrl = 'https://your-ngrok-url.ngrok.io/frontend/';
const keyboard = {
    inline_keyboard: [[
        {
            text: 'Open Bridge Exchange',
            web_app: { url: webAppUrl }
        }
    ]]
};
```

## 🔄 Demo Flow

The demo flow simulates a complete user journey:

1. **Login** - Telegram WebApp authentication
2. **Deposit** - Create CryptoPay invoice
3. **Payment** - Simulate webhook payment
4. **Trading** - Place buy/sell orders
5. **AI Analysis** - Get portfolio recommendations
6. **Withdrawal** - Create withdrawal request
7. **Additional Features** - NFT minting, P2P, staking

## 🏗️ Architecture

### Database Schema

- **Users** - User accounts and profiles
- **Wallets** - Multi-asset wallet addresses
- **Balances** - Asset balances and reserves
- **Transactions** - All financial transactions
- **Orders** - Trading orders and orderbook
- **Trades** - Executed trades
- **NFTs** - NFT items and metadata
- **P2P** - Peer-to-peer offers
- **Stakes** - Staking positions
- **DAO** - Governance proposals
- **Tickets** - Support tickets
- **Admin Logs** - Administrative actions

### API Endpoints

#### Authentication
- `POST /api/auth/telegram_login` - Login with Telegram
- `GET /api/auth/me` - Get current user

#### Wallet
- `POST /api/wallet/deposit` - Create deposit
- `POST /api/wallet/withdraw` - Create withdrawal
- `GET /api/wallet/balances/{user_id}` - Get balances
- `POST /api/wallet/transfer` - Internal transfer
- `POST /api/wallet/crypto/webhook` - CryptoPay webhook

#### Exchange
- `POST /api/exchange/order` - Place order
- `POST /api/exchange/cancel` - Cancel order
- `GET /api/exchange/orderbook` - Get order book
- `GET /api/exchange/trades` - Get trade history

#### NFT
- `POST /api/nft/mint` - Mint NFT
- `GET /api/nft/listings` - Get marketplace
- `POST /api/nft/buy` - Buy NFT

#### P2P
- `POST /api/p2p/offer` - Create offer
- `POST /api/p2p/accept` - Accept offer
- `POST /api/p2p/release` - Release funds

#### Staking
- `POST /api/stake/stake` - Create stake
- `POST /api/stake/unstake` - Unstake tokens
- `POST /api/stake/claim_rewards` - Claim rewards

#### DAO
- `POST /api/dao/proposal` - Create proposal
- `POST /api/dao/vote` - Vote on proposal
- `GET /api/dao/proposals` - Get proposals

#### AI Assistant
- `POST /api/ai/portfolio` - Analyze portfolio
- `POST /api/ai/chat` - Chat with AI
- `POST /api/ai/trading_signal` - Get trading signal

#### Admin
- `GET /api/admin/stats` - Get statistics
- `POST /api/admin/adjust_balance` - Adjust balance
- `POST /api/admin/freeze_user` - Freeze user
- `POST /api/admin/refund` - Process refund

#### Support
- `POST /api/support/ticket` - Create ticket
- `POST /api/support/message` - Add message
- `GET /api/support/tickets` - Get tickets

## 🔒 Security Features

- **JWT Authentication** - Secure token-based auth
- **Webhook Verification** - CryptoPay signature validation
- **Rate Limiting** - API rate limiting
- **Input Validation** - Pydantic schema validation
- **SQL Injection Protection** - SQLAlchemy ORM
- **CORS Configuration** - Cross-origin security
- **Admin Permissions** - Role-based access control

## 🚀 Deployment

### Local Development
```bash
# Backend
uvicorn backend.main:app --reload --port 8000

# Frontend (serve static files)
# Use any static file server or ngrok
```

### Production Deployment

1. **Database**: Use PostgreSQL instead of SQLite
2. **Redis**: Add Redis for caching and rate limiting
3. **HTTPS**: Use proper SSL certificates
4. **Environment**: Set production environment variables
5. **Monitoring**: Add logging and monitoring
6. **Scaling**: Use load balancers and multiple instances

## 📊 Monitoring & Alerts

### Background Jobs
- **Invoice Polling** - Check pending payments
- **Price Updates** - Update cryptocurrency prices
- **Staking Rewards** - Calculate and distribute rewards
- **Transaction Reconciliation** - Verify external transactions
- **API Health Checks** - Monitor external services

### Admin Dashboard
- User statistics and activity
- Transaction monitoring
- Balance reconciliation
- Support ticket management
- System health monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the demo flow
- Test with the provided examples

## 🔮 Future Enhancements

- **Mobile App** - React Native mobile application
- **Advanced Trading** - Futures, options, margin trading
- **DeFi Integration** - Yield farming, liquidity pools
- **Cross-Chain** - Multi-blockchain support
- **Advanced AI** - More sophisticated AI features
- **Social Trading** - Copy trading, social features
- **Institutional Features** - OTC trading, prime brokerage

---

**⚠️ Important**: This is a demonstration project. For production use, ensure proper security audits, compliance with regulations, and adequate testing.
