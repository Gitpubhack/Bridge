# Bridge Exchange - Quick Start Guide

## 🚀 Быстрый запуск

### 1. Установка зависимостей
```bash
cd /Users/admin/Documents/bridgebot
pip3 install -r backend/requirements_minimal.txt
```

### 2. Запуск сервера
```bash
cd /Users/admin/Documents/bridgebot
python3 -m uvicorn backend.main_simple:app --reload --port 8002
```

### 3. Проверка работы
- API доступен по адресу: http://localhost:8002
- Документация API: http://localhost:8002/docs
- Health check: http://localhost:8002/health

## 📁 Структура проекта

```
bridgebot/
├── backend/                 # FastAPI backend
│   ├── main_simple.py      # Простая версия без БД
│   ├── main.py             # Полная версия с БД
│   ├── models/             # SQLAlchemy модели
│   ├── schemas/            # Pydantic схемы
│   ├── routers/            # API роутеры
│   ├── services/           # Внешние API клиенты
│   └── config.py           # Конфигурация
├── frontend/               # Telegram WebApp
│   ├── index.html          # Главная страница
│   └── assets/             # CSS и JS
├── scripts/                # Утилиты
└── README.md               # Полная документация
```

## 🔧 Настройка

### Конфигурация API ключей
Скопируйте `backend/config.example.py` в `backend/config.py` и заполните:

```python
# Telegram Bot
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"

# CryptoPay
CRYPTOPAY_API_TOKEN = "YOUR_CRYPTOPAY_TOKEN"
CRYPTOPAY_API_HOST = "https://pay.crypt.bot"

# Bybit
BYBIT_API_KEY = "YOUR_BYBIT_KEY"
BYBIT_API_SECRET = "YOUR_BYBIT_SECRET"

# TON API
TONAPI_KEY = "YOUR_TONAPI_KEY"

# OpenAI
OPENAI_API_KEY = "YOUR_OPENAI_KEY"
```

## 🧪 Тестирование

### Запуск тестов
```bash
cd backend
pytest tests/
```

### Демо сценарий
```bash
python3 scripts/demo_flow.py
```

## 🌐 Ngrok для Telegram WebApp

### Установка ngrok
```bash
# Скачайте ngrok с https://ngrok.com/download
# Или через Homebrew:
brew install ngrok
```

### Запуск ngrok
```bash
./scripts/run_ngrok.sh 8002
```

### Настройка Telegram Bot
1. Создайте бота через @BotFather
2. Установите WebApp URL: `https://your-ngrok-url.ngrok.io/frontend/index.html`

## 📱 Frontend

Откройте в браузере: http://localhost:8002/frontend/index.html

## 🐛 Решение проблем

### Порт занят
```bash
# Найдите процесс на порту 8002
lsof -i :8002

# Убейте процесс
kill -9 PID
```

### Ошибки импорта
Убедитесь, что вы находитесь в корневой директории проекта:
```bash
cd /Users/admin/Documents/bridgebot
```

### Проблемы с зависимостями
```bash
# Переустановите зависимости
pip3 uninstall -r backend/requirements_minimal.txt -y
pip3 install -r backend/requirements_minimal.txt
```

## 📞 Поддержка

Если у вас возникли проблемы:
1. Проверьте логи сервера
2. Убедитесь, что все зависимости установлены
3. Проверьте конфигурацию в `config.py`
4. Обратитесь к полной документации в `README.md`
