from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys


# Параметры подключения к PostgreSQL
DB_HOST = "localhost"
DB_NAME = "star_db"
APP_USER = "constellation_user"
APP_PASSWORD = "mizorit"

# Подключение к базе данных с использованием созданного пользователя
def create_database_engine():
    try:
        DATABASE_URL = f"postgresql+psycopg2://{APP_USER}:{APP_PASSWORD}@{DB_HOST}/{DB_NAME}"
        engine = create_engine(DATABASE_URL, echo=True)

        # Проверяем подключение
        with engine.connect() as conn:
            pass

        return engine

    except OperationalError as e:
        error_msg = str(e.orig)

        sys.stderr.write(str(e) + "\n\n")

        if 'пользователь "' in error_msg and '" не прошёл проверку подлинности' in error_msg:
            sys.stderr.write('ОШИБКА: Пользователь constellation_user не существует, запустите скрипт install_db.bat')
        elif 'пользователь "' in error_msg and '" не существует' in error_msg:
            sys.stderr.write('ОШИБКА: Пользователь constellation_user не существует, запустите скрипт install_db.bat')
        elif 'база данных "' in error_msg and '" не существует' in error_msg:
            sys.stderr.write('ОШИБКА: База данных star_db не существует, запустите скрипт install_db.bat')
        else:
            sys.stderr.write(f'ОШИБКА подключения к базе данных: {error_msg}')

        sys.exit(1)
    except ProgrammingError as e:
        sys.stderr.write(f'ОШИБКА SQL: {str(e)}')
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f'НЕИЗВЕСТНАЯ ОШИБКА: {str(e)}')
        sys.exit(1)

# Создание фабрики сессий
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()