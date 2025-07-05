@echo off
setlocal enabledelayedexpansion
set PG_PATH="C:\Program Files\PostgreSQL\17\bin\psql.exe"
set NEW_USER=constellation_user
set NEW_PASSWORD=mizorit
set DB_NAME=star_db

:input_password
set /p PG_PASSWORD="Введите пароль пользователя postgres: "
if "!PG_PASSWORD!"=="" goto input_password

set PGPASSWORD=!PG_PASSWORD!

:: Создание пользователя
!PG_PATH! -U postgres -c "CREATE USER !NEW_USER! WITH PASSWORD '!NEW_PASSWORD!';" 2>nul && (
    echo Пользователь !NEW_USER! создан
) || (
    echo Пользователь !NEW_USER! уже существует
)

:: Создание БД
!PG_PATH! -U postgres -c "CREATE DATABASE !DB_NAME! WITH OWNER !NEW_USER!;" 2>nul && (
    echo База данных !DB_NAME! создана
) || (
    echo База данных !DB_NAME! уже существует
)

:: Создание временного файла с SQL-командами
echo GRANT CONNECT ON DATABASE !DB_NAME! TO !NEW_USER!; > grants.sql
echo GRANT USAGE, CREATE ON SCHEMA public TO !NEW_USER!; >> grants.sql
echo ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO !NEW_USER!; >> grants.sql
echo ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO !NEW_USER!; >> grants.sql
echo GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO !NEW_USER!; >> grants.sql
echo GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO !NEW_USER!; >> grants.sql

:: Выполнение SQL-команд из файла
!PG_PATH! -U postgres -d !DB_NAME! -f grants.sql

:: Удаление временного файла
del grants.sql

echo.
echo Настройка прав завершена:
echo - Пользователь: !NEW_USER!
echo - Может создавать таблицы в схеме public
echo - Имеет полные права на свои таблицы
echo - Может читать/изменять существующие таблицы
pause