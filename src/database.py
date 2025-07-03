from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2 import sql
import logging
import os
import sys

def get_db_state_path():
    if getattr(sys, 'frozen', False):
        # Если программа запущена как exe (PyInstaller)
        base_path = sys._MEIPASS
    else:
        # Обычный запуск через Python
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'src', 'db_state.txt')

# Параметры подключения к PostgreSQL
DB_HOST = "localhost"
DB_NAME = "star_db"
APP_USER = "constellation_user"
APP_PASSWORD = "mizorit"

# Файл для кэширования состояния базы данных
DB_STATE_FILE = get_db_state_path()

# Подключение к базе данных с использованием созданного пользователя
DATABASE_URL = f"postgresql+psycopg2://{APP_USER}:{APP_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()