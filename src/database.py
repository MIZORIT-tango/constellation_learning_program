from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2 import sql
import logging
import os

# Параметры подключения к PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"  # Суперпользователь
DB_PASSWORD = "mizorit"  # Пароль суперпользователя
DB_NAME = "star_db"
APP_USER = "constellation_user"
APP_PASSWORD = "mizorit"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Файл для кэширования состояния базы данных
DB_STATE_FILE = "db_state.txt"

# Функция для создания пользователя, если он не существует
def create_user_if_not_exists():
    try:
        # Подключение к PostgreSQL с использованием суперпользователя
        with psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                # Проверка существования пользователя
                cursor.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (APP_USER,))
                exists = cursor.fetchone()

                if not exists:
                    # Создание пользователя
                    cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(APP_USER)), (APP_PASSWORD,))
                    logger.info(f"Пользователь '{APP_USER}' создан.")
                else:
                    logger.info(f"Пользователь '{APP_USER}' уже существует.")
    except Exception as e:
        logger.error(f"Ошибка при создании пользователя: {e}")

# Функция для создания базы данных, если она не существует
def create_database_if_not_exists():
    try:
        # Подключение к PostgreSQL с использованием суперпользователя
        with psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                # Проверка существования базы данных
                cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,))
                exists = cursor.fetchone()

                if not exists:
                    # Создание базы данных
                    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
                    logger.info(f"База данных '{DB_NAME}' создана.")
                else:
                    logger.info(f"База данных '{DB_NAME}' уже существует.")
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {e}")

# Функция для назначения прав пользователю
def grant_privileges():
    try:
        # Подключение к PostgreSQL с использованием суперпользователя
        with psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                # Назначение прав пользователю
                cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                    sql.Identifier(DB_NAME),
                    sql.Identifier(APP_USER)
                ))
                cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {}").format(
                    sql.Identifier(APP_USER)
                ))
                cursor.execute(sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO {}").format(
                    sql.Identifier(APP_USER)
                ))
                logger.info(f"Права назначены пользователю '{APP_USER}'.")
    except Exception as e:
        logger.error(f"Ошибка при назначении прав: {e}")

# Функция для проверки состояния базы данных
def check_db_state():
    if os.path.exists(DB_STATE_FILE):
        with open(DB_STATE_FILE, 'r') as f:
            return f.read().strip() == "initialized"
    return False

# Функция для установки состояния базы данных
def set_db_state(state):
    with open(DB_STATE_FILE, 'w') as f:
        f.write(state)

# Основная функция для инициализации базы данных
def initialize_database():
    if not check_db_state():
        create_user_if_not_exists()
        create_database_if_not_exists()
        grant_privileges()
        set_db_state("initialized")
    else:
        logger.info("База данных уже инициализирована.")

# Инициализация базы данных
initialize_database()

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