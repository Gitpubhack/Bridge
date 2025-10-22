"""
Простое приложение Bridge Exchange
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Создаем приложение
app = FastAPI(
    title="Bridge Exchange",
    description="Простое приложение для тестирования",
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
        "message": "Bridge Exchange работает!",
        "status": "OK",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    """Проверка здоровья"""
    return {"status": "healthy"}

@app.get("/api/test")
async def test():
    """Тестовый эндпоинт"""
    return {
        "message": "API работает!",
        "data": {
            "user_id": 1,
            "balance": "1000 USDT"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
