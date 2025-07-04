from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Параметры подключения к PostgreSQL
DB_HOST = "localhost"
DB_NAME = "star_db"
APP_USER = "constellation_user"
APP_PASSWORD = "mizorit"

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