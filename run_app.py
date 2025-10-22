#!/usr/bin/env python3
"""
Запуск Bridge Exchange приложения
"""
import sys
import os

# Добавляем backend в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Импортируем и запускаем
from main_simple_fixed import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)
