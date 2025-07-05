# program for memorizing constellations

## Описание

На данный момент приложение показывает вам изображение созвездия, а вы должны угадать его название. Включает 87 официальных созвездий. Сохраняет фотографии в PosgreSQL

## Установка

Для установки выполните следующие шаги:

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/mizorit-tango/constellation_learning_program.git
    ```

2. Перейдите в директорию проекта:

    ```bash
    cd constellation_learning_program
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

### Установка PostgreSQL

Для работы требуется PostgreSQL. Следуйте этим шагам для установки PostgreSQL:

1. Скачайте и установите PostgreSQL с [официального сайта PostgreSQL](https://www.postgresql.org/download/).
2. Настройте сервер PostgreSQL, следуя инструкциям на экране.
3. Создайте базу данных и пользователя.

## Настройка PostgreSQL
Приложение требует PostgreSQL для хранения данных.

### Автоматическая настройка:

Запустите install_db.bat – он создаст:

* Базу данных: constellation_db

* Пользователя: constellation_user с паролем mizorit

# Запуск

## Запуск через main.exe (рекомендуется)

1. Запустите main.exe

## Из исходного кода

Для запуска приложения выполните следующие шаги:

1. Запустите приложение с помощью команды:

    ```bash
    python src/main.py
    ```

## Запуск через main.exe (с его созданием)

1. Запустите скрипт build.bat

   ```bash
   start build.bat
   ```
   
2. Перейдите в папку dist

   ```bash
   cd dist
   ```
   
3. Запустите main.exe

   ```bash
   start main.exe
   ```