@echo off
set PG_PATH="C:\Program Files\PostgreSQL\17\bin\psql.exe"
set NEW_USER=constellation_user
set NEW_PASSWORD=mizorit
set DB_NAME=star_db

:input_password
set /p PG_PASSWORD="Введите пароль пользователя postgres: "
if "%PG_PASSWORD%"=="" goto input_password

set PGPASSWORD=%PG_PASSWORD%

:: Создание пользователя (упрощенная версия)
%PG_PATH% -U postgres -c "CREATE USER %NEW_USER% WITH PASSWORD '%NEW_PASSWORD%';" 2>nul && (
    echo Пользователь %NEW_USER% создан
) || (
    echo Пользователь %NEW_USER% уже существует
)

:: Создание БД
%PG_PATH% -U postgres -c "CREATE DATABASE %DB_NAME% OWNER %NEW_USER%;" 2>nul && (
    echo База данных %DB_NAME% создана
) || (
    echo База данных %DB_NAME% уже существует
)

%PG_PATH% -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO %NEW_USER%;"

echo.
echo Данные для подключения:
echo Пользователь: %NEW_USER%
echo Пароль: %NEW_PASSWORD%
echo База данных: %DB_NAME%
pause